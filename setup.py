from setuptools import setup
from torch.utils.cpp_extension import CUDAExtension, BuildExtension
import os

root_dir = os.path.dirname(os.path.abspath(__file__))

# Compiler flags for Windows CUDA 11.8 + VS 2022 compatibility
cxx_flags = []
nvcc_flags = ["-I" + os.path.join(root_dir, "lib/glm/")]

if os.name == 'nt':  # Windows
    cxx_flags = [
        '/D_ALLOW_COMPILER_AND_STL_VERSION_MISMATCH',
        '/D_SILENCE_ALL_CXX17_DEPRECATION_WARNINGS',
    ]
    nvcc_flags.extend([
        '-allow-unsupported-compiler',
        '-D_ALLOW_COMPILER_AND_STL_VERSION_MISMATCH',
        '--expt-relaxed-constexpr',
        '--expt-extended-lambda',
    ])

extra_compile_args = {
    'cxx': cxx_flags,
    'nvcc': nvcc_flags
}

setup(
    name="diffoctreerast",
    version="0.1.0",
    author="Jianfeng Xiang",
    description="Differential Octree Rasterization for 3D Generation",
    packages=['diffoctreerast'],
    ext_modules=[
        CUDAExtension(
            name="diffoctreerast._C",
            sources=[
                # Octree Voxel rasterization
                "src/octree_voxel_rasterizer/cuda/data_structure.cu",
                "src/octree_voxel_rasterizer/cuda/forward.cu",
                "src/octree_voxel_rasterizer/cuda/backward.cu",
                "src/octree_voxel_rasterizer/api.cpp",
                # Octree Gaussian rasterization
                "src/octree_gaussian_rasterizer/cuda/data_structure.cu",
                "src/octree_gaussian_rasterizer/cuda/forward.cu",
                "src/octree_gaussian_rasterizer/cuda/backward.cu",
                "src/octree_gaussian_rasterizer/api.cpp",
                # Octree Trivec rasterization
                "src/octree_trivec_rasterizer/cuda/data_structure.cu",
                "src/octree_trivec_rasterizer/cuda/forward.cu",
                "src/octree_trivec_rasterizer/cuda/backward.cu",
                "src/octree_trivec_rasterizer/api.cpp",
                # Octree Decoupled Polynomial rasterization
                "src/octree_decoupoly_rasterizer/cuda/data_structure.cu",
                "src/octree_decoupoly_rasterizer/cuda/forward.cu",
                "src/octree_decoupoly_rasterizer/cuda/backward.cu",
                "src/octree_decoupoly_rasterizer/api.cpp",
                # Main
                "src/ext.cpp"
            ],
            extra_compile_args=extra_compile_args,
        )
    ],
    cmdclass={
        'build_ext': BuildExtension
    }
)
