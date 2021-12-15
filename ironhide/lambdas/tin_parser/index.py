"""
TIN parser lambda
"""

import logging
import traceback
import json
from typing import Dict, Any

from ironhide.parsers.tin import TINParser


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event: Dict[str, Any], lambda_context: Dict[str, Any]):
    """
    Handle events for TIN parsing.
    """

    message = json.loads(event["Records"][0]["body"])

    try:
        tins = TINParser.parse(message)
        return tins
    except Exception:  # pylint: disable=broad-except
        logger.error("Lambda Error")
        logger.error(traceback.format_exc())
        return False
