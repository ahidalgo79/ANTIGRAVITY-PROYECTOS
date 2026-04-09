import pandas as pd

path = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS\Fichas_Analisis_NUEVO.xlsx'

def get_stats():
    try:
        # Load the stats sheet
        df_stats = pd.read_excel(path, sheet_name='ESTADISTICAS')
        print("--- ESTADISTICAS START ---")
        print(df_stats.to_string())
        print("--- ESTADISTICAS END ---")
        
        # Also check TODOS_PAPERS for total count and relevance
        df_papers = pd.read_excel(path, sheet_name='TODOS_PAPERS')
        print(f"\nTotal Papers Analyzed: {len(df_papers)}")
        
        if 'Relevancia' in df_papers.columns:
            relevance = df_papers['Relevancia'].value_counts()
            print("\nRelevance Distribution:")
            print(relevance)
            
        if 'Algoritmo Principal' in df_papers.columns:
            algos = df_papers['Algoritmo Principal'].value_counts()
            print("\nAlgorithm Distribution:")
            print(algos)

        if 'Dominio Aplicación' in df_papers.columns:
            domains = df_papers['Dominio Aplicación'].value_counts()
            print("\nDomain Distribution:")
            print(domains)
            
    except Exception as e:
        print(f"Error reading Excel: {e}")

if __name__ == "__main__":
    get_stats()
