import numpy as np
from join_matmul import TableJoinMatmul

class TableJoinNumpy(TableJoinMatmul):

    def matmul(self, mat_a : np.ndarray, mat_b : np.ndarray) -> np.ndarray:
        return np.dot(mat_a, mat_b)