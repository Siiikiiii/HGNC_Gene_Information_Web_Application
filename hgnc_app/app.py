from flask import Flask, request, render_template
from pathlib import Path
import logging
from typing import Dict, Any, Optional

from hgnc_app import settings
from hgnc_app.models import data_parser
from hgnc_app.logger import setup_logging


# -------------------------------------------------------------------
# Application Factory
# -------------------------------------------------------------------
def create_app() -> Flask:
    """
    Create and configure the Flask application.

    This function encapsulates application creation to avoid
    global side-effects and allow flexible configuration.

    Returns
    -------
    Flask
        Configured Flask application instance.
    """

    # Create Flask instance (NOT at import time anymore)
    app: Flask = Flask(__name__)

    # ---------------------------------------------------------------
    # Logging setup
    # ---------------------------------------------------------------
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Initialising Flask application via factory")

    # ---------------------------------------------------------------
    # Load data (now happens ONCE when app is created)
    # ---------------------------------------------------------------
    DATA_FILE = settings.DATA_FILE

    logger.info(f"Loading data from {DATA_FILE}")

    try:
        # Store data inside app config to avoid global state
        # ✅ This is important for testing and flexibility
        app.config["DATA"] = data_parser.read_file(DATA_FILE)
        logger.info("Data loaded successfully")

    except Exception:
        logger.exception("Failed to load data")
        raise

    # ---------------------------------------------------------------
    # Routes
    # ---------------------------------------------------------------

    @app.route("/")
    def home() -> str:
        """
        Render the homepage.

        Returns
        -------
        str
            Rendered HTML template.
        """
        logger.debug("Rendering homepage")
        return render_template("index.html")

    @app.route("/search", methods=["POST"])
    def search() -> str:
        """
        Handle gene search requests.

        This endpoint retrieves a gene information including previous symbols, aliases,
        and MANE transcripts form input (i.e., an HGNC-approved gene symbol or an HGNC ID)
        and queries the dataset loaded at application creation.

        Returns
        -------
        str
            Rendered template containing results or error messages.
        """
        try:
            query: str = request.form.get("gene", "").strip()
            logger.debug(f"Received search request for gene: {query}")

            # -------------------------------------------------------
            # Validate input
            # -------------------------------------------------------
            if not query:
                logger.warning("No search term provided")
                return render_template(
                    "index.html",
                    error_message="Error: No search term provided. Please enter a gene symbol or HGNC ID.",
                )

            # -------------------------------------------------------
            # Retrieve data from app config (NOT global variable)
            # -------------------------------------------------------
            data: Dict[str, Any] = app.config["DATA"]

            selection: Optional[Dict[str, Any]] = data_parser.find_gene(query, data)

            if selection is None:
                logger.info(f"Gene not found: {query}")
                return render_template(
                    "index.html",
                    error_message=f"Error: Gene '{query}' not found"
                )

            logger.info(f"Gene found: {query}")

            return render_template("index.html", gene_data=selection)

        except KeyError as e:
            logger.warning(f"Missing expected data field: {e}")
            return render_template(
                "index.html",
                error_message=f"Error: missing data field {str(e)}"
            )

        except Exception as e:
            logger.exception("Unexpected error during search")
            return render_template(
                "index.html",
                error_message=f"Error: {str(e)}"
            )

    return app

# -------------------------------------------------------------------
# Application instance (for mounting to gunicorn or mod_wsgi)
# -------------------------------------------------------------------
app: Flask = create_app()


# -------------------------------------------------------------------
# Entry point (local development only)
# -------------------------------------------------------------------
if __name__ == "__main__":
    logging.getLogger(__name__).info("Running Flask app")
    app.run()