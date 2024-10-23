from triton_matmul import matmul
import torch
import numpy as np
from join_matmul import TableJoinMatmul


class TableJoinTriton(TableJoinMatmul):

    def matmul(self, mat_a : np.ndarray, mat_b : np.ndarray) -> np.ndarray:
        torch_mat_a = torch.tensor(mat_a, dtype=torch.float16, device='cuda')
        torch_mat_b = torch.tensor(mat_b, dtype=torch.float16, device='cuda')
        return matmul(torch_mat_a, torch_mat_b).cpu().numpy()