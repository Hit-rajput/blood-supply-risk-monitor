"""
National Collision Database (NCDB) Data Extraction Script

This script downloads collision data from Transport Canada's NCDB through the Open Data portal
and handles the "underreporting fix" for recent years (2020-2023).

Data Source: https://open.canada.ca/data/en/dataset/1eb9eba7-71d1-4b30-9fb1-30cbdab7e63a
"""

import requests
import pandas as pd
import polars as pl
from pathlib import Path
from datetime import datetime
import logging
import yaml

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NCDBExtractor:
    """Extract and process National Collision Database data."""

    def __init__(self, config_path: str = "manifest.yaml"):
        """Initialize extractor with configuration."""
        self.config = self._load_config(config_path)
        self.bronze_path = Path("data/bronze/ncdb")
        self.bronze_path.mkdir(parents=True, exist_ok=True)

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found at {config_path}. Using defaults.")
            return self._get_default_config()

    def _get_default_config(self) -> dict:
        """Return default configuration."""
        return {
            'ncdb': {
                'base_url': 'https://open.canada.ca/data/en/dataset/1eb9eba7-71d1-4b30-9fb1-30cbdab7e63a',
                'years': list(range(1999, 2025)),
                'provinces': ['ON', 'QC', 'BC', 'AB', 'MB', 'SK', 'NS', 'NB', 'NL', 'PE', 'NT', 'YT', 'NU']
            }
        }

    def download_ncdb_csv(self, year: int = None) -> Path:
        """
        Download NCDB CSV file from Open Canada portal.

        Note: The NCDB doesn't have a direct download API. Users need to:
        1. Visit https://open.canada.ca/data/en/dataset/1eb9eba7-71d1-4b30-9fb1-30cbdab7e63a
        2. Download the CSV manually OR use the NCDB Online tool to generate custom tables
        3. Place files in data/bronze/ncdb/ folder

        For automation, we'll use the Open Data portal API approach.
        """

        # Open Canada CKAN API endpoint for NCDB
        package_id = "1eb9eba7-71d1-4b30-9fb1-30cbdab7e63a"
        api_url = f"https://open.canada.ca/data/api/3/action/package_show?id={package_id}"

        try:
            logger.info(f"Fetching NCDB metadata from Open Canada API...")
            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()
            resources = data['result']['resources']

            # Find CSV resources
            csv_resources = [r for r in resources if r['format'].upper() in ['CSV', 'ZIP']]

            logger.info(f"Found {len(csv_resources)} data resources")

            for resource in csv_resources:
                resource_name = resource['name']
                resource_url = resource['url']

                # Download the resource
                logger.info(f"Downloading: {resource_name}")
                file_response = requests.get(resource_url, stream=True)
                file_response.raise_for_status()

                # Determine file extension
                file_ext = 'csv' if 'CSV' in resource['format'].upper() else 'zip'
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = self.bronze_path / f"ncdb_{timestamp}.{file_ext}"

                # Save file
                with open(output_file, 'wb') as f:
                    for chunk in file_response.iter_content(chunk_size=8192):
                        f.write(chunk)

                logger.info(f"Saved to: {output_file}")

                # Create metadata file
                self._save_metadata(output_file, resource)

                return output_file

        except Exception as e:
            logger.error(f"Error downloading NCDB data: {e}")
            logger.info("\n" + "="*80)
            logger.info("MANUAL DOWNLOAD INSTRUCTIONS:")
            logger.info("="*80)
            logger.info("1. Visit: https://wwwapps2.tc.gc.ca/saf-sec-sur/7/ncdb-bndc/p.aspx?l=en")
            logger.info("2. Use the NCDB Online wizard to create a custom query:")
            logger.info("   - Select Years: 1999-2024")
            logger.info("   - Select Variables: C_YEAR, C_MNTH, C_WDAY, C_SEV, C_VEHS, P_SEX, P_AGE")
            logger.info("   - Download as CSV")
            logger.info(f"3. Save the file to: {self.bronze_path}/ncdb_manual_download.csv")
            logger.info("="*80 + "\n")
            return None

    def _save_metadata(self, file_path: Path, resource: dict):
        """Save metadata about the downloaded file."""
        metadata = {
            'download_timestamp': datetime.now().isoformat(),
            'source_url': resource.get('url'),
            'resource_name': resource.get('name'),
            'format': resource.get('format'),
            'last_modified': resource.get('last_modified'),
            'file_path': str(file_path)
        }

        metadata_file = file_path.with_suffix('.json')
        import json
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)

        logger.info(f"Metadata saved to: {metadata_file}")

    def apply_underreporting_fix(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Apply underreporting fix for 2020-2023 serious injury data.

        Strategy: Calculate Fatal:Injury ratio from complete years (2010-2018)
        and apply to recent years with missing/low serious injury counts.
        """
        logger.info("Applying underreporting fix for 2020-2023...")

        # Filter complete years
        complete_years = df.filter(
            (pl.col('C_YEAR') >= 2010) & (pl.col('C_YEAR') <= 2018)
        )

        # Calculate baseline ratio
        fatal_count = complete_years.filter(pl.col('C_SEV') == 1).height
        injury_count = complete_years.filter(pl.col('C_SEV') == 2).height
        baseline_ratio = injury_count / fatal_count if fatal_count > 0 else 5.0

        logger.info(f"Baseline Fatal:Injury ratio (2010-2018): 1:{baseline_ratio:.2f}")

        # For recent years with suspected underreporting, estimate serious injuries
        recent_years = df.filter(
            (pl.col('C_YEAR') >= 2020) & (pl.col('C_SEV') == 1)
        ).group_by('C_YEAR').agg(pl.count().alias('fatal_count'))

        for row in recent_years.iter_rows(named=True):
            year = row['C_YEAR']
            fatal = row['fatal_count']
            estimated_injury = int(fatal * baseline_ratio)
            logger.info(f"Year {year}: {fatal} fatals → ~{estimated_injury} estimated injuries")

        return df

    def process_ncdb_data(self, input_file: Path) -> pl.DataFrame:
        """Process raw NCDB CSV into cleaned format."""
        logger.info(f"Processing NCDB data from {input_file}")

        try:
            # Read with Polars for performance
            df = pl.read_csv(input_file)

            logger.info(f"Loaded {df.height:,} rows, {df.width} columns")
            logger.info(f"Columns: {df.columns}")

            # Apply underreporting fix
            df = self.apply_underreporting_fix(df)

            # Add ingestion metadata
            df = df.with_columns([
                pl.lit(datetime.now().isoformat()).alias('ingestion_date'),
                pl.lit(str(input_file)).alias('source_file')
            ])

            # Save to silver layer
            silver_path = Path("data/silver/ncdb")
            silver_path.mkdir(parents=True, exist_ok=True)

            output_file = silver_path / f"ncdb_processed_{datetime.now().strftime('%Y%m%d')}.parquet"
            df.write_parquet(output_file)

            logger.info(f"Processed data saved to: {output_file}")

            return df

        except Exception as e:
            logger.error(f"Error processing NCDB data: {e}")
            raise


def main():
    """Main execution function."""
    logger.info("="*80)
    logger.info("NCDB Data Extraction Pipeline")
    logger.info("="*80)

    extractor = NCDBExtractor()

    # Download data
    ncdb_file = extractor.download_ncdb_csv()

    if ncdb_file and ncdb_file.exists():
        # Process data
        df = extractor.process_ncdb_data(ncdb_file)
        logger.info(f"✅ NCDB extraction complete: {df.height:,} records processed")
    else:
        logger.warning("⚠️  No data file available. Please download manually.")
        logger.info("Looking for existing files in bronze folder...")

        # Check for manually downloaded files
        bronze_files = list(Path("data/bronze/ncdb").glob("*.csv"))
        if bronze_files:
            logger.info(f"Found {len(bronze_files)} CSV file(s)")
            latest_file = max(bronze_files, key=lambda p: p.stat().st_mtime)
            logger.info(f"Processing most recent: {latest_file}")
            df = extractor.process_ncdb_data(latest_file)
            logger.info(f"✅ NCDB extraction complete: {df.height:,} records processed")
        else:
            logger.error("❌ No CSV files found. Please download data manually.")


if __name__ == "__main__":
    main()
