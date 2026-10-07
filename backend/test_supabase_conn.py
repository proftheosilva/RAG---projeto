import os
import sys
from dotenv import load_dotenv
import httpx

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
# Test with SECRET_KEY or PUBLISHABLE_KEY
supabase_key = os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_PUBLISHABLE_KEY")

if not supabase_url or not supabase_key:
    print("SUPABASE: falha na conexão (variáveis de ambiente não encontradas)")
    sys.exit(1)

try:
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}"
    }
    # Test request to Supabase REST root or OpenAPI spec
    response = httpx.get(f"{supabase_url}/rest/v1/", headers=headers, timeout=10.0)
    
    if response.status_code in (200, 404, 401, 403):
        # Let's verify valid auth response
        if response.status_code == 200:
            print("SUPABASE: conexão estabelecida com sucesso")
            sys.exit(0)
        else:
            # Maybe rest/v1/ returns openapi spec or 200
            print(f"SUPABASE: resposta da API com status {response.status_code}")
            # If 401/403, key may have permission or format issue
            if response.status_code in (401, 403):
                print("SUPABASE: falha na conexão (autenticação recusada)")
                sys.exit(1)
            else:
                print("SUPABASE: conexão estabelecida com sucesso")
                sys.exit(0)
    else:
        print("SUPABASE: falha na conexão")
        sys.exit(1)
except Exception as e:
    print(f"SUPABASE: falha na conexão")
    sys.exit(1)
