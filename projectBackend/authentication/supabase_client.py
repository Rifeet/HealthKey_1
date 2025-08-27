from supabase import create_client
import os

class SupabaseClient:
    @staticmethod
    def get_client():
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        return create_client(url, key)

    @staticmethod
    def get_service_client():
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        return create_client(url, key)