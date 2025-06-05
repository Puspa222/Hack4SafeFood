import logging
from django.core.management.base import BaseCommand
from chat.vector_service import vector_service

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Initialize ChromaDB vector store with PDF documents'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force-recreate',
            action='store_true',
            help='Force recreate the vector store even if it exists',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Starting ChromaDB vector store initialization...')
        )

        force_recreate = options.get('force_recreate', False)
        
        try:
            success = vector_service.initialize(force_recreate=force_recreate)
            
            if success:
                self.stdout.write(
                    self.style.SUCCESS('✅ Vector store initialized successfully!')
                )
                
                # Test the vector store
                test_query = "pesticide safety"
                results = vector_service.similarity_search(test_query, k=2)
                
                if results:
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ Vector store test successful - found {len(results)} relevant documents')
                    )
                    for i, doc in enumerate(results, 1):
                        source = doc.metadata.get('source', 'Unknown')
                        content_preview = doc.page_content[:100] + "..." if len(doc.page_content) > 100 else doc.page_content
                        self.stdout.write(f"  {i}. {source}: {content_preview}")
                else:
                    self.stdout.write(
                        self.style.WARNING('⚠️ Vector store created but test search returned no results')
                    )
            else:
                self.stdout.write(
                    self.style.ERROR('❌ Failed to initialize vector store')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error during initialization: {str(e)}')
            )
