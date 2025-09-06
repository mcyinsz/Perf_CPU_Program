#include <iostream>
#include <vector>
#include <random>
#include <chrono>

// generating random matrix
std::vector<std::vector<double>> generateRandomMatrix(int rows, int cols) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<double> dis(0.0, 10.0);
    
    std::vector<std::vector<double>> matrix(rows, std::vector<double>(cols));
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            matrix[i][j] = dis(gen);
        }
    }
    return matrix;
}

// execute matrix multiplication
std::vector<std::vector<double>> matrixMultiply(
    const std::vector<std::vector<double>>& A,
    const std::vector<std::vector<double>>& B) {
    
    int M = A.size();
    int K = A[0].size();
    int N = B[0].size();
    
    std::vector<std::vector<double>> C(M, std::vector<double>(N, 0.0));
    
    for (int i = 0; i < M; ++i) {
        for (int j = 0; j < N; ++j) {
            for (int k = 0; k < K; ++k) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
    
    return C;
}

// print matrix
void printMatrix(const std::vector<std::vector<double>>& matrix, int maxRows = 5, int maxCols = 5) {
    int rows = matrix.size();
    int cols = matrix[0].size();
    
    std::cout << "Matrix [" << rows << " x " << cols << "]:\n";
    
    for (int i = 0; i < std::min(rows, maxRows); ++i) {
        for (int j = 0; j < std::min(cols, maxCols); ++j) {
            std::cout << matrix[i][j] << "\t";
        }
        if (cols > maxCols) std::cout << "...";
        std::cout << "\n";
    }
    if (rows > maxRows) std::cout << "...\n";
    std::cout << "\n";
}

int main(int argc, char* argv[]) {
    // default matrix dimensions
    int M = 3;
    int K = 4;
    int N = 5;
    
    // get matrix dimension params from cmd param
    if (argc >= 4) {
        M = std::atoi(argv[1]);
        K = std::atoi(argv[2]);
        N = std::atoi(argv[3]);
    }
    
    std::cout << "Generating matrices [" << M << "," << K << "] and [" << K << "," << N << "]...\n";
    
    // get input matrices
    auto A = generateRandomMatrix(M, K);
    auto B = generateRandomMatrix(K, N);
    
    std::cout << "Matrix A:\n";
    printMatrix(A);
    
    std::cout << "Matrix B:\n";
    printMatrix(B);
    
    // execute matrix multiplication
    auto start = std::chrono::high_resolution_clock::now();
    auto C = matrixMultiply(A, B);
    auto end = std::chrono::high_resolution_clock::now();
    
    std::chrono::duration<double> duration = end - start;
    
    std::cout << "Result matrix C (A * B):\n";
    printMatrix(C);
    
    std::cout << "Multiplication took " << duration.count() << " seconds.\n";
    
    return 0;
}