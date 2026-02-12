# AI Reading List - Categorized

## GPU Architecture & Hardware

- [Cornell Virtual Workshop: Understanding GPU Architecture](https://cvw.cac.cornell.edu/gpu-architecture)
- [How to Think About GPUs | How To Scale Your Model](https://jax-ml.github.io/scaling-book/gpus/)
- [How to think about GPU](https://x.com/soumithchintala/status/2a2d3915504381ccaa96e9277535f8b5) (tweet)
- [Inside NVIDIA GPUs: Anatomy of high performance matmul kernels - Aleksa Gordić](https://www.aleksagordic.com/blog/matmul)
- [GPU L2 Cache Persistence | simons blog](https://veitner.bearblog.dev/gpu-l2-cache-persistence/)
- [AMD Data Center GPUs Explained: MI250X, MI300X, MI350X and Beyond](https://www.bentoml.com/blog/amd-data-center-gpus-mi250x-mi300x-mi350x-and-beyond)
- [Tenstorrent Blackhole, Grendel, And Buda – A Scale Out Architecture](https://semianalysis.com/2022/04/12/tenstorrent-blackhole-grendel-and/)
- [$2 H100s: How the GPU Bubble Burst - by Eugene Cheah](https://www.latent.space/p/gpu-bubble)
- [Fire-Flyer AI-HPC: A Cost-Effective Software-Hardware Co-Design for Deep Learning](https://arxiv.org/abs/2408.14158)
- [The Data Center is the New Compute Unit: Nvidia's Vision for System-Level Scaling](https://www.fabricatedknowledge.com/p/the-data-center-is-the-new-compute)
- [KVBM Architecture — NVIDIA Dynamo Documentation](https://docs.nvidia.com/dynamo/latest/kvbm/kvbm_architecture.html)
- [Understanding Peak, Max-Achievable & Delivered FLOPs, Part 1 — ROCm Blogs](https://rocm.blogs.amd.com/software-tools-optimization/Understanding_Peak_and_Max-Achievable_FLOPS/README.html)
- [Measuring the environmental impact of AI inference | Google Cloud Blog](https://cloud.google.com/blog/products/infrastructure/measuring-the-environmental-impact-of-ai-inference)
- [mikeroyal/GPU-Guide: Graphics Processing Unit (GPU) Architecture Guide](https://github.com/mikeroyal/GPU-Guide#Parallel-Computing)

## CUDA & Kernel Programming

- [How to Optimize a CUDA Matmul Kernel for cuBLAS-like Performance: a Worklog](https://siboehm.com/articles/22/CUDA-MMM)
- [Learning CUDA by optimizing softmax: A worklog | Maharshi's blog](https://blog.prajwal.work/learning-cuda-by-optimizing-softmax-a-worklog)
- [Erkaman/Awesome-CUDA: This is a list of useful libraries and resources for CUDA development](https://github.com/Erkaman/Awesome-CUDA)
- [PacktPublishing/Hands-On-GPU-Programming-with-Python-and-CUDA](https://github.com/PacktPublishing/Hands-On-GPU-Programming-with-Python-and-CUDA)
- [NVIDIA/cuda-samples: Samples for CUDA Developers](https://github.com/NVIDIA/cuda-samples)
- [BBuf/how-to-optim-algorithm-in-cuda: how to optimize some algorithm in cuda](https://github.com/BBuf/how-to-optim-algorithm-in-cuda)
- [CUTLASS Tutorial: Writing GEMM Kernels Using Tensor Memory For NVIDIA® Blackwell GPUs – Colfax Research](https://research.colfax-intl.com/cutlass-tutorial-writing-gemm-kernels-using-tensor-memory-for-nvidia-blackwell-gpus/)
- [Getting Started With CuTe — NVIDIA CUTLASS Documentation](https://docs.nvidia.com/cutlass/media/docs/cpp/cute/00_quickstart.html)
- [Surprisingly Fast AI-Generated Kernels We Didn't Mean to Publish (Yet) | Scaling Intelligence Lab at Stanford](https://scalingintelligence.stanford.edu/blogs/fastkernels/)
- [Making Deep Learning go Brrrr From First Principles](https://horace.io/brrr_intro.html)
- [A Manual Implementation of Quantization in PyTorch - Single Layer - Hexo](http://example.com/2024/05/16/quantization-1/)

## ML Compilers & Frameworks

- [Glow: Compiler for Neural Network hardware accelerators](https://arxiv.org/abs/1805.00907)
- [ML Compilers Part 2: An Overview of Graph Optimizations - FuzzyWare](https://uditagarwal.in/ml-compilers-part-2-graph-optimizations/)
- [Pallas Design — JAX documentation](https://jax.readthedocs.io/en/latest/pallas/design.html)
- [Autodidax: JAX core from scratch — JAX documentation](https://jax.readthedocs.io/en/latest/autodidax.html)
- [OpenXLA is available now to accelerate and simplify machine learning | Google Open Source Blog](https://opensource.googleblog.com/2023/03/openxla-is-ready-to-accelerate-and-simplify-ml-development.html?m=1)
- [(4) Accelerate PyTorch workloads with PyTorch/XLA - YouTube](https://www.youtube.com/watch?v=PSpmRtWuMs8&t=1s&ab_channel=GoogleCloudTech)
- [Ways to use torch.compile : ezyang's blog](http://blog.ezyang.com/2024/11/ways-to-use-torch-compile/)
- [Meta PyTorch Team 2024 H2 Roadmaps - PyTorch Developer Mailing List](https://dev-discuss.pytorch.org/t/meta-pytorch-team-2024-h2-roadmaps/2226)
- [Making WAF ML models go brrr: saving decades of processing time](https://blog.cloudflare.com/making-waf-ai-models-go-brr)

## LLM Inference & Serving Systems

- [vLLM v0.6.0: 2.7x Throughput Improvement and 5x Latency Reduction | vLLM Blog](https://blog.vllm.ai/2024/09/05/perf-update.html)
- [Paged Attention from First Principles: A View Inside vLLM | Hamza's Blog](https://hamzaelshafie.bearblog.dev/paged-attention-from-first-principles-a-view-inside-vllm/)
- [\[RFC\] PagedAttention Support · Issue #121465 · pytorch/pytorch](https://github.com/pytorch/pytorch/issues/121465)
- [SGLang v0.4: Zero-Overhead Batch Scheduler, Cache-Aware Load Balancer, Faster Structured Outputs | LMSYS Org](https://lmsys.org/blog/2024-12-04-sglang-v0-4/?utm_source=perplexity)
- [sglang pdf](https://arxiv.org/abs/2312.07104)
- [flash decoding](https://crfm.stanford.edu/2023/10/12/flashdecoding.html)
- [Dissecting Batching Effects in GPT Inference](https://le.qun.ch/en/blog/2023/05/13/transformer-batching/)
- [TensorRT-LLM Architecture — tensorrt_llm documentation](https://docs.nvidia.com/deeplearning/tensorrt/tensorrt-llm/architecture/)
- [TensorRT-LLM Architecture — TensorRT-LLM](https://nvidia.github.io/TensorRT-LLM/architecture/overview.html)
- [TensorRT explained | aijobs.net](https://aijobs.net/insights/tensorrt-explained/)
- [Triton Architecture — NVIDIA Triton Inference Server](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/architecture.html#ensemble-models)
- [Welcome to Model Optimizer (ModelOpt) documentation!](https://nvidia.github.io/TensorRT-Model-Optimizer/)
- [Speculative cascades — A hybrid approach for smarter, faster LLM inference](https://research.google/blog/speculative-cascades-a-hybrid-approach-for-smarter-faster-llm-inference/)
- [Medusa: Simple framework for accelerating LLM generation with multiple decoding heads](https://www.together.ai/blog/medusa)
- [\[2408.04093\] Tree Attention: Topology-aware Decoding for Long-Context Attention on GPU clusters](https://arxiv.org/abs/2408.04093)
- [Disaggregated Inference at Scale with PyTorch & vLLM – PyTorch](https://pytorch.org/blog/disaggregated-inference-at-scale-with-pytorch-vllm/)
- [Disaggregated Inference at Scale with PyTorch & vLLM – PyTorch](https://share.google/NW6syhhx0uyxYMAce) (second copy)
- [Deploying DeepSeek with PD Disaggregation and Large-Scale Expert Parallelism on 96 H100 GPUs | LMSYS Org](https://lmsys.org/blog/2025-05-05-large-scale-ep/)
- [How multi-node inference works for massive LLMs like DeepSeek-R1 | Baseten Blog](https://www.baseten.co/blog/how-multi-node-inference-works-llms-deepseek-r1/)
- [GitHub - MoonshotAI/checkpoint-engine: Checkpoint-engine is a simple middleware to update model weights in LLM inference engines](https://github.com/MoonshotAI/checkpoint-engine)
- [Why do LLM input tokens cost less than output tokens?](https://peterchng.com/blog/2024/05/01/why-do-llm-input-tokens-cost-less-than-output-tokens/)
- [Azure/kaito: Kubernetes AI Toolchain Operator](https://github.com/Azure/kaito)
- [Integrating NVIDIA TensorRT-LLM with the Databricks Inference Stack | Databricks Blog](https://www.databricks.com/blog/Integrating-NVIDIA-TensorRT-LLM)

## Distributed Training & Scaling

- [\[2105.04663\] GSPMD: General and Scalable Parallelization for ML Computation Graphs](https://arxiv.org/abs/2105.04663)
- [Cloud TPU Multislice Overview \[Public Preview\] | Google Cloud](https://cloud.google.com/tpu/docs/multislice-introduction#optimize)
- [ZeRO & DeepSpeed: New system optimizations enable training models with over 100 billion parameters - Microsoft Research](https://www.microsoft.com/en-us/research/blog/zero-deepspeed-new-system-optimizations-enable-training-models-with-over-100-billion-parameters/)
- [The Ultra-Scale Playbook - a Hugging Face Space by nanotron](https://huggingface.co/spaces/nanotron/ultrascale-playbook)
- [LLM训练终极指南 | The Ultra-Scale Playbook - a Hugging Face Space by Ki-Seki](https://huggingface.co/spaces/Ki-Seki/ultrascale-playbook-zh-cn)
- [How To Scale Your Model](https://jax-ml.github.io/scaling-book/)
- [Prime Intellect: OpenDiLoCo](https://www.primeintellect.ai/blog/opendiloco)
- [X OpenDiLoCo](https://x.com/1f19597ac93c41bbac652ab5ed19450c) (tweet)
- [INTELLECT-1 Release The First Globally Trained 10B Parameter Model](https://www.primeintellect.ai/blog/intellect-1-release)
- [prime/INTELLECT_1_Technical_Report.pdf at main · PrimeIntellect-ai/prime](https://github.com/PrimeIntellect-ai/prime/blob/main/INTELLECT_1_Technical_Report.pdf)
- [Weight Transfer for RL Post-Training in under 2 seconds](https://research.perplexity.ai/articles/weight-transfer-for-rl-post-training-in-under-2-seconds)

## LLM Architecture & Fundamentals

- [The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/llm-architecture-showdown)
- [Transformer Architecture: The Positional Encoding - Amirhossein Kazemnejad's Blog](https://kazemnejad.com/blog/transformer_architecture_positional_encoding/)
- [\[2405.17927v1\] The Evolution of Multimodal Model Architectures](https://arxiv.org/abs/2405.17927v1)
- [Speech and Language Processing](https://web.stanford.edu/~jurafsky/slp3/)
- [\[2501.09223\] Foundations of Large Language Models (this is a book)](https://arxiv.org/abs/2501.09223)
- [What's Really Going On in Machine Learning? Some Minimal Models—Stephen Wolfram Writings](https://writings.stephenwolfram.com/2024/08/whats-really-going-on-in-machine-learning-some-minimal-models/)
- [\[2406.02528\] Scalable MatMul-free Language Modeling](https://arxiv.org/abs/2406.02528)
- [\[2403.06963\] The pitfalls of next-token prediction](https://arxiv.org/abs/2403.06963)
- [Are all LLMs really 1.58 bits? Inference at 4x the speed or more?](https://learning-exhaust.hashnode.dev/are-all-large-language-models-really-in-158-bits)
- [\[1806.08342\] Quantizing deep convolutional networks for efficient inference: A whitepaper](https://arxiv.org/abs/1806.08342)
- [Quantization aware training | TensorFlow Model Optimization](https://www.tensorflow.org/model_optimization/guide/quantization/training)
- [vllm quantization](https://x.com/14bd391550438139867fc566f8315d30) (tweet)

## State Space Models (Mamba)

- [What do I need to know about Mamba in the ML world](https://www.perplexity.ai/search/e5e57674-6a3b-4093-80ef-00f280fd7336)
- [Mamba No. 5 (A Little Bit Of…) | Sparse Notes](https://jameschen.io/jekyll/update/2024/02/12/mamba.html)
- [Mamba: The Easy Way](https://jackcook.com/2024/02/23/mamba.html)
- [Mamba: The Hard Way](https://srush.github.io/annotated-mamba/hard.html)

## Reasoning, Reinforcement Learning & Post-Training

- [Late Takes on OpenAI o1](https://www.interconnects.ai/p/late-takes-on-openai-o1)
- [Scaling test-time compute - a Hugging Face Space by HuggingFaceH4](https://huggingface.co/spaces/HuggingFaceH4/blogpost-scaling-test-time-compute)
- [\[2408.03314\] Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters](https://arxiv.org/abs/2408.03314)
- [Post-training 101](https://www.interconnects.ai/p/post-training-101)
- [Post-training 101 | Tokens for Thoughts](https://philschmid.de/post-training)
- [A Primer on LLM Post-Training – PyTorch](https://pytorch.org/blog/a-primer-on-llm-post-training/)
- [The N Implementation Details of RLHF with PPO | ICLR Blogposts 2024](https://iclr-blogposts.github.io/2024/blog/the-n-implementation-details-of-rlhf-with-ppo/)
- [RLHF Book by Nathan Lambert](https://rlhfbook.com/)
- [Reinforcement learning from AI feedback (RLAIF): Complete overview | SuperAnnotate](https://www.superannotate.com/blog/reinforcement-learning-from-ai-feedback-rlaif)
- [TAO: Using test-time compute to train efficient LLMs without labeled data | Databricks Blog](https://www.databricks.com/blog/tao-using-test-time-compute-train-efficient-llms-without-labeled-data)
- [Online RL for Cursor Tab | Cursor - The AI Code Editor](https://cursor.com/blog/tab-rl)
- [Improving Cursor Tab With RL | Cursor - The AI Code Editor](https://cursor.com/en/blog/tab-rl)
- [\[2507.10605\] RedOne: Revealing Domain-specific LLM Post-Training in Social Networking Services](https://arxiv.org/abs/2507.10605)

## Fine-Tuning & Training Techniques

- [Practical Tips for Finetuning LLMs Using LoRA (Low-Rank Adaptation)](https://magazine.sebastianraschka.com/p/practical-tips-for-finetuning-llms)
- [Improving LoRA: Implementing Weight-Decomposed Low-Rank Adaptation (DoRA) from Scratch](https://magazine.sebastianraschka.com/p/lora-and-dora-from-scratch)
- [Distilling Llama3.1 8B into 1B in torchtune | PyTorch](https://pytorch.org/blog/llama-into-torchtune/)
- [Training great LLMs entirely from ground zero in the wilderness as a startup — Yi Tay](https://www.yitay.net/blog/training-great-llms-entirely-from-ground-zero-in-the-wilderness)
- [Large Language Models, How to Train Them, and xAI's Grok](https://chamath.substack.com/p/large-language-models-how-to-train)
- [\[2403.05440\] Is Cosine-Similarity of Embeddings Really About Similarity?](https://arxiv.org/abs/2403.05440)
- [Human-like systematic generalization through a meta-learning neural network | Nature](https://www.nature.com/articles/s41586-023-06668-3)
- [The Training Imperative](https://sdan.io/blog/training-imperative)

## AI Agents & Tools

- [Agents](https://huyenchip.com/2025/01/07/agents.html)
- [Building effective agents \\ Anthropic](https://www.anthropic.com/research/building-effective-agents)
- [We need to talk about Agents...](https://mikeroyal.medium.com/we-need-to-talk-about-agents-a9e2b4f0e0e5)
- [x.com Meta Agent](https://x.com/jeffclune/status/1825551351746867502) (tweet)
- [Why I No Longer Recommend RAG for Autonomous Coding Agents](https://pashpashpash.substack.com/p/why-i-no-longer-recommend-rag-for)
- [tom-doerr/awesome-dspy](https://github.com/tom-doerr/awesome-dspy)

## RAG & Information Retrieval

- [Advanced RAG Techniques: an Illustrated Overview | by IVAN ILIN | Towards AI](https://pub.towardsai.net/advanced-rag-techniques-an-illustrated-overview-04d193d8fec6)
- [Will Amazon S3 Vectors Kill Vector Databases—or Save Them? - Zilliz blog](https://milvus.io/blog/will-amazon-s3-vectors-kill-vector-databases-or-save-them)

## LLM Safety, Alignment & Interpretability

- [Adversarial Attacks on LLMs | Lil'Log](https://lilianweng.github.io/posts/2024-01-10-adversarial-attacks/)
- [Many-shot jailbreaking \\ Anthropic](https://www.anthropic.com/research/many-shot-jailbreaking)
- [Claude's Character \\ Anthropic](https://www.anthropic.com/research/claude-character)
- [Extrinsic Hallucinations in LLMs | Lil'Log](https://lilianweng.github.io/posts/2024-07-07-hallucination/)
- [\[2410.05229\] GSM-Symbolic: Understanding the Limitations of Mathematical Reasoning in Large Language Models](https://arxiv.org/abs/2410.05229)
- [Circuit Tracing: Revealing Computational Graphs in Language Models](https://transformer-circuits.pub/2025/attribution-graphs/methods.html)
- [On the Biology of a Large Language Model](https://transformer-circuits.pub/2025/attribution-graphs/biology.html)
- [SolidGoldMagikarp (plus, prompt generation) — LessWrong](https://www.lesswrong.com/posts/aPeJE8bSo6rAFoLqg/solidgoldmagikarp-plus-prompt-generation)
- [Explaining SolidGoldMagikarp by looking at it from random directions — LessWrong](https://www.lesswrong.com/posts/jbi9kxhb4iCQyWG9Y/explaining-solidgoldmagikarp-by-looking-at-it-from-random)

## Specific Model Releases & Analysis

- [Introducing Apple's On-Device and Server Foundation Models - Apple Machine Learning Research](https://machinelearning.apple.com/research/introducing-apple-foundation-models)
- [Apple Foundation Model](https://arxiv.org/abs/2407.21075)
- [Qwen 2: a story of Alibaba vs Meta - by Rick Lamers](https://codingwithintelligence.com/p/qwen-2-a-story-of-alibaba-vs-meta)
- [Qwen 3](https://qwenlm.github.io/blog/qwen3/)
- [Introducing Mixtral 8x7B with Databricks Model Serving | Databricks Blog](https://www.databricks.com/blog/introducing-mixtral-8x7b-databricks-model-serving)
- [Getting Started with Mixtral 8X7B | Pinecone](https://www.pinecone.io/learn/mixtral-8x7b/)
- [Dario Amodei — On DeepSeek and Export Controls](https://darioamodei.com/on-deepseek-and-export-controls)
- [xAI's Grok 4: The tension of frontier performance with a side of Elon favoritism](https://www.interconnects.ai/p/grok-4-an-o3-look-alike-in-search)
- [Claude 3.5 Sonnet Insane Coding Ability](https://claude3.pro/claude-3-5-sonnet-insane-coding-ability/)
- [\[2502.15964\] Minions: Cost-efficient Collaboration Between On-device and Cloud Language Models](https://arxiv.org/abs/2502.15964)

## AI Industry, Opinion & Commentary

- [What I Wish Someone Had Told Me - Sam Altman](https://blog.samaltman.com/what-i-wish-someone-had-told-me)
- [Dear VC's, please stop throwing money at AI founders with no commercial plan, besides AGI](https://substack.recursal.ai/cp/143397465)
- [What can LLMs never do? - by Rohit Krishnan](https://www.strangeloopcanon.com/p/what-can-llms-never-do)
- [On AI for developer productivity](https://simonwillison.net/2024/Dec/13/on-ai-for-developer-productivity/)
- [OpenAI: Facts from a Weekend — LessWrong](https://www.lesswrong.com/posts/KXHMCH7wCxrvKsJyn/openai-facts-from-a-weekend)
- [AI 2027](https://ai-2027.com/)
- [LLM evolution](https://chat.openai.com/share/dead-link) (dead ChatGPT link)
- [Ilya Sutskever: The brain behind ChatGPT](https://journeymatters.ai/ilya-the-brain-behind-chatgpt/)
- [Ilya's recom to Carmack](https://x.com/aeae1dae348a413989d4baf60f3055af) (tweet)
- [The Way of Code | Rick Rubin](https://wayofcode.com/)

## Vision, Multimodal & Robotics

- [V-JEPA: The next step toward advanced machine intelligence](https://ai.meta.com/blog/v-jepa-yann-lecun-ai-model-video-joint-embedding-predictive-architecture/)
- [OpenVLA: An Open-Source Vision-Language-Action Model](https://openvla.github.io/)
- [Video Generation Models Explosion 2024 - Yen-Chen Lin](https://yenchenlin.github.io/blog/2025/01/08/video-generation-models-explosion-2024/)

## Research Overviews & Curated Lists

- [10 Noteworthy AI Research Papers of 2023](https://magazine.sebastianraschka.com/p/10-ai-research-papers-2023)
- [Research Papers in January 2024 - by Sebastian Raschka, PhD](https://magazine.sebastianraschka.com/p/research-papers-in-january-2024)
- [2024 best papers](https://magazine.sebastianraschka.com/p/2024-best-papers)
- [The 2025 AI Engineering Reading List - Latent.Space](https://www.latent.space/p/2025-papers)
- [GitHub - mlabonne/llm-course: Course to get into Large Language Models (LLMs) with roadmaps and Colab notebooks](https://github.com/mlabonne/llm-course)
- [adithya-s-k/AI-Engineering.academy: Mastering Applied AI, One Concept at a Time](https://github.com/adithya-s-k/AI-Engineering.academy)
- [GitHub - dair-ai/ML-YouTube-Courses: 📺 Discover the latest machine learning / AI courses on YouTube](https://github.com/dair-ai/ML-YouTube-Courses)
- [GitHub - zhaochenyang20/Awesome-ML-SYS-Tutorial: My learning notes/codes for ML SYS](https://github.com/zhaochenyang20/Awesome-ML-SYS-Tutorial)
- [Archive • AI News • Buttondown](https://buttondown.com/ainews/archive/)
- [Hugging Face – Blog](https://huggingface.co/blog)

## Crypto, Decentralized AI & Misc

- [The promise and challenges of crypto + AI applications](https://vitalik.eth.limo/general/2024/01/30/cryptoai.html)
- [A checklist for switching to open source ML models](https://www.baseten.co/blog/a-checklist-for-switching-to-open-source-ml-models/)
- [Modular Manifolds - Thinking Machines Lab](https://thinkingmachines.ai/blog/modular-manifolds/)

## Classic ML & Deep Learning

- [At the Intersection of LLMs and Kernels - Research Roundup](http://charlesfrye.github.io/programming/2023/11/10/llms-systems.html)
- [\[2311.08360\] The Transient Nature of Emergent In-Context Learning in Transformers](https://arxiv.org/abs/2311.08360)
- [Distill — Latest articles about machine learning](https://distill.pub/)
- [Techniques for training large neural networks](https://openai.com/research/techniques-for-training-large-neural-networks)

## Tweets (topic unclear / unreadable content)

- [x.com](https://x.com/soumithchintala/status/1841498799652708712) - dynamic sparse attention related
- [x.com](https://x.com/realgeorgehotz/status/1874924715414040679) - George Hotz tweet
- [Page title...](https://x.com/6b129a5cbdc4434bb9fdba33cb20b258) - tweet about in-context learning
- [Ben Thimpson podcast](https://x.com/882ff35bdb504a03a6892fd4c84d23e5) (tweet link)
- [q star info.pdf - Google Drive](https://drive.google.com/file/d/1xlRDbMUDE41XPzwStAGyAVEP8qA9Tna7/view)

## Non-AI / Systems / Misc

- [My Fave New Podcasts of 2023](https://www.swyx.io/podcasts-2023)
- [AI at Scale - Microsoft Research](https://www.microsoft.com/en-us/research/project/ai-at-scale/)
- [Stanford CRFM](https://crfm.stanford.edu/2025/05/28/fast-kernels.html)
- [FunSearch: Making new discoveries in mathematical sciences using Large Language Models - Google DeepMind](https://deepmind.google/discover/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/)
- [How Does BitTorrent Work? A Plain English Guide](https://skerritt.blog/bit-torrent/)
- [EndpointSlices | Kubernetes](https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/)
- [Borg: The Predecessor to Kubernetes | Kubernetes](https://kubernetes.io/blog/2015/04/borg-predecessor-to-kubernetes/)
- [Borg: the Next Generation](https://research.google/pubs/borg-the-next-generation/)
- [Kubernetes API Concepts | Kubernetes](https://kubernetes.io/docs/reference/using-api/concepts/)
- [system observability // simo.sh](https://simo.sh/blog/system-observability)
- [quick note April 19, 2025](https://www.notion.so/1dbd3915504380808c6ec94d0e0f4cbd) (personal note)

## Deep RL

- [Welcome to the 🤗 Deep Reinforcement Learning Course - Hugging Face Deep RL Course](https://huggingface.co/learn/deep-rl-course/unit0/introduction)

---

## External URLs (from "From an old list" section)

- [A Brief History of TensorFlow Extended (TFX)](https://blog.tensorflow.org/2020/09/brief-history-of-tensorflow-extended-tfx.html)
- [An Introduction To HuggingFace Transformers for NLP](https://wandb.ai/int_pb/huggingface/reports/An-Introduction-To-HuggingFace-Transformers-for-NLP--VmlldzoyOTgzMjI5)
- [Function calling and other API updates - OpenAI](https://openai.com/blog/function-calling-and-other-api-updates)
- [Neural Network Architectures Guide](https://www.v7labs.com/blog/neural-network-architectures-guide)
- [Neural Network Architectures - Medium](https://towardsdatascience.com/neural-network-architectures-156e5bad51ba)
- [Information Theory, Inference and Learning Algorithms](https://www.inference.org.uk/mackay/itila/)
