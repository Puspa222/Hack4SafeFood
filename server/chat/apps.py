from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'

    def ready(self):
        """Load existing vectorstore when Django app starts (no re-embedding)"""
        try:
            from .vector_service_new import vector_service
            logger.info("Loading existing vectorstore on app startup...")
            # Only load existing vectorstore, don't recreate
            vector_service.load_existing_vectorstore()
            logger.info("Vectorstore loading completed")
        except Exception as e:
            logger.error(f"Failed to load vectorstore on startup: {e}")
