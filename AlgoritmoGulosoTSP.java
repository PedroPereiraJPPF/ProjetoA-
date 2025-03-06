import java.util.Arrays;

public class AlgoritmoGulosoTSP {
    private static final int INF = Integer.MAX_VALUE; // Representa a ausência de aresta
    
    public static void main(String[] args) {
        int[][] grafo = {
            {INF, 10, 20, 15},
            {10, INF, 35, 25},
            {20, 35, INF, 30},
            {15, 25, 30, INF}
        };
        
        encontrarTourMinimo(grafo, 0);
    }

    public static void encontrarTourMinimo(int[][] grafo, int inicio) {
        int n = grafo.length;
        boolean[] visitado = new boolean[n];
        int[] tour = new int[n + 1]; 
        int custoTotal = 0;
        
        int atual = inicio;
        visitado[atual] = true;
        tour[0] = atual;

        for (int i = 1; i < n; i++) {
            int proximo = -1;
            int menorCusto = INF;
            
            for (int j = 0; j < n; j++) {
                if (!visitado[j] && grafo[atual][j] < menorCusto) {
                    menorCusto = grafo[atual][j];
                    proximo = j;
                }
            }
            
            if (proximo == -1) break;
            
            visitado[proximo] = true;
            tour[i] = proximo;
            custoTotal += menorCusto;
            atual = proximo;
        }
        
        // Volta ao ponto inicial para completar o ciclo (se possível)
        if (grafo[atual][inicio] != INF) {
            tour[n] = inicio;
            custoTotal += grafo[atual][inicio];
        } else {
            System.out.println("Não foi possível encontrar um ciclo.");
            return;
        }
        
        System.out.println("Tour encontrado: " + Arrays.toString(Arrays.stream(tour).map(i -> i + 1).toArray()));
        System.out.println("Custo total: " + custoTotal);
    }
}