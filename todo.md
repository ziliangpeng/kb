# Research TODO

## Datacenter Training Networking

Research datacenter training network topologies in depth:

- Fat-tree topology and its limitations at scale
- Rail-optimized topologies
- InfiniBand vs Ethernet tradeoffs at 100K+ GPU scale
- DWDM (wavelength-division multiplexing) for inter-site links
- DiLoCo and other semi-synchronous training approaches
- How the communication hierarchy maps to parallelism strategies

## Triton Developer Conference 2025

Watch and take notes on the 3rd Triton Developer Conference (October 21, 2025, Microsoft Silicon Valley Campus).

- **Playlist**: https://www.youtube.com/playlist?list=PLc_vA1r0qoiQqCdWFDUDqI90oY5EjfGuO
- **Channel**: https://www.youtube.com/@Triton-openai/videos

Full talk list:

1. Jason Taylor — Welcome to the Triton Developer Conference
2. Phil Tillet and Thomas Raoux — Triton Today and Beyond
3. Mark Saroufim — The State of Triton in OSS Communities
4. Jason Ansel — Helion: A High-level DSL for ML Kernels
5. Keren Zhou and Yuanwei Fang — Proton: Portable Performance Profiling
6. Lixun Zhang — Triton's Day One Speed on AMD GPUs
7. Chris Sullivan — A Performance Engineer's Guide to NVIDIA Blackwell GPUs
8. Peter Bell and Jeff Niu — Gluon: Tile-Based GPU Programming with Low-level Control
9. Hongtao Yu — TLX: Minimally Invasive Paths to Performance Portability
10. Wenlei Bao — Trion: Distributed Programming — Overlapping Kernels on Distributed AI Systems with Triton C
11. Yanning Chen and Vaibhav Jindal — Evolution of Liger Kernels to Post-training
