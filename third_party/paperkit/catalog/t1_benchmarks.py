"""Papers and public benchmarks (arXiv IDs) for the T1 datasets in regen_map.py.

PAPERS: every arXiv ID used below, with title / first author / date pulled from the
arXiv API on 2026-09-21 (verified, not typed from memory).
ROWS:   dataset -> papers behind the data, public benchmarks it feeds or is evaluated on,
        benchmarks without an arXiv ID, and a note grounded in the card or the paper text.
DOMAIN: domain-wide public benchmarks relevant to simulator-generated Physical AI data.
"""
PAPERS = {
 "2503.14734": {
  "short": "GR00T N1",
  "title": "GR00T N1: An Open Foundation Model for Generalist Humanoid Robots",
  "first_author": " NVIDIA",
  "date": "2025-03"
 },
 "2410.24185": {
  "short": "DexMimicGen",
  "title": "DexMimicGen: Automated Data Generation for Bimanual Dexterous Manipulation via Imitation Learning",
  "first_author": "Zhenyu Jiang",
  "date": "2024-10"
 },
 "2406.02523": {
  "short": "RoboCasa",
  "title": "RoboCasa: Large-Scale Simulation of Everyday Tasks for Generalist Robots",
  "first_author": "Soroush Nasiriany",
  "date": "2024-06"
 },
 "2310.17596": {
  "short": "MimicGen",
  "title": "MimicGen: A Data Generation System for Scalable Robot Learning using Human Demonstrations",
  "first_author": "Ajay Mandlekar",
  "date": "2023-10"
 },
 "2511.04831": {
  "short": "Isaac Lab",
  "title": "Isaac Lab: A GPU-Accelerated Simulation Framework for Multi-Modal Robot Learning",
  "first_author": " NVIDIA",
  "date": "2025-11"
 },
 "2606.03551": {
  "short": "Isaac Sim",
  "title": "NVIDIA Isaac Sim: Enabling Scalable, GPU-Accelerated Simulation for Robotics",
  "first_author": "Sicong Gao",
  "date": "2026-06"
 },
 "2306.03310": {
  "short": "LIBERO",
  "title": "LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning",
  "first_author": "Bo Liu",
  "date": "2023-06"
 },
 "2405.05941": {
  "short": "SimplerEnv",
  "title": "Evaluating Real-World Robot Manipulation Policies in Simulation",
  "first_author": "Xuanlin Li",
  "date": "2024-05"
 },
 "2506.18123": {
  "short": "RoboArena",
  "title": "RoboArena: Distributed Real-World Evaluation of Generalist Robot Policies",
  "first_author": "Pranav Atreya",
  "date": "2025-06"
 },
 "2403.09227": {
  "short": "BEHAVIOR-1K",
  "title": "BEHAVIOR-1K: A Human-Centered, Embodied AI Benchmark with 1,000 Everyday Activities and Realistic Simulation",
  "first_author": "Chengshu Li",
  "date": "2024-03"
 },
 "2112.03227": {
  "short": "CALVIN",
  "title": "CALVIN: A Benchmark for Language-Conditioned Policy Learning for Long-Horizon Robot Manipulation Tasks",
  "first_author": "Oier Mees",
  "date": "2021-12"
 },
 "2410.00425": {
  "short": "ManiSkill3",
  "title": "ManiSkill3: GPU Parallelized Robotics Simulation and Rendering for Generalizable Embodied AI",
  "first_author": "Stone Tao",
  "date": "2024-10"
 },
 "2009.12293": {
  "short": "robosuite",
  "title": "robosuite: A Modular Simulation Framework and Benchmark for Robot Learning",
  "first_author": "Yuke Zhu",
  "date": "2020-09"
 },
 "2403.12945": {
  "short": "DROID",
  "title": "DROID: A Large-Scale In-The-Wild Robot Manipulation Dataset",
  "first_author": "Alexander Khazatsky",
  "date": "2024-03"
 },
 "2310.08864": {
  "short": "Open X-Embodiment",
  "title": "Open X-Embodiment: Robotic Learning Datasets and RT-X Models",
  "first_author": "Open X-Embodiment Collaboration",
  "date": "2023-10"
 },
 "2606.02800": {
  "short": "Cosmos 3",
  "title": "Cosmos 3: Omnimodal World Models for Physical AI",
  "first_author": " NVIDIA",
  "date": "2026-06"
 },
 "2501.03575": {
  "short": "Cosmos WFM",
  "title": "Cosmos World Foundation Model Platform for Physical AI",
  "first_author": " NVIDIA",
  "date": "2025-01"
 },
 "2503.15558": {
  "short": "Cosmos-Reason1",
  "title": "Cosmos-Reason1: From Physical Common Sense To Embodied Reasoning",
  "first_author": " NVIDIA",
  "date": "2025-03"
 },
 "2503.14492": {
  "short": "Cosmos-Transfer1",
  "title": "Cosmos-Transfer1: Conditional World Generation with Adaptive Multimodal Control",
  "first_author": " NVIDIA",
  "date": "2025-03"
 },
 "2506.09042": {
  "short": "Cosmos-Drive-Dreams",
  "title": "Cosmos-Drive-Dreams: Scalable Synthetic Driving Data Generation with World Foundation Models",
  "first_author": "Xuanchi Ren",
  "date": "2025-06"
 },
 "2511.00062": {
  "short": "Cosmos-Predict2.5 report",
  "title": "World Simulation with Video Foundation Models for Physical AI",
  "first_author": " NVIDIA",
  "date": "2025-10"
 },
 "2512.01989": {
  "short": "PAI-Bench",
  "title": "PAI-Bench: A Comprehensive Benchmark For Physical AI",
  "first_author": "Fengzhe Zhou",
  "date": "2025-12"
 },
 "2501.09038": {
  "short": "Physics-IQ",
  "title": "Do generative video models understand physical principles?",
  "first_author": "Saman Motamed",
  "date": "2025-01"
 },
 "2311.17982": {
  "short": "VBench",
  "title": "VBench: Comprehensive Benchmark Suite for Video Generative Models",
  "first_author": "Ziqi Huang",
  "date": "2023-11"
 },
 "2502.20694": {
  "short": "WorldModelBench",
  "title": "WorldModelBench: Judging Video Generation Models As World Models",
  "first_author": "Dacheng Li",
  "date": "2025-02"
 },
 "2601.21282": {
  "short": "WorldBench",
  "title": "WorldBench: Benchmarking Physical Understanding of World Models by Isolating Physics Concepts",
  "first_author": "Rishi Upadhyay",
  "date": "2026-01"
 },
 "2410.05363": {
  "short": "PhyGenBench",
  "title": "Towards World Simulator: Crafting Physical Commonsense-Based Benchmark for Video Generation",
  "first_author": "Fanqing Meng",
  "date": "2024-10"
 },
 "2507.13428": {
  "short": "PhyWorldBench",
  "title": "\"PhyWorldBench\": A Comprehensive Evaluation of Physical Realism in Text-to-Video Models",
  "first_author": "Jing Gu",
  "date": "2025-07"
 },
 "2412.12507": {
  "short": "3DGUT",
  "title": "3DGUT: Enabling Distorted Cameras and Secondary Rays in Gaussian Splatting",
  "first_author": "Qi Wu",
  "date": "2024-12"
 },
 "2407.07090": {
  "short": "3DGRT",
  "title": "3D Gaussian Ray Tracing: Fast Tracing of Particle Scenes",
  "first_author": "Nicolas Moenne-Loccoz",
  "date": "2024-07"
 },
 "2607.14203": {
  "short": "Instant NuRec",
  "title": "Instant NuRec: Feed-Forward 3D Gaussian Reconstruction for Driving Scene Simulation",
  "first_author": " NVIDIA",
  "date": "2026-07"
 },
 "1912.04838": {
  "short": "Waymo Open Dataset",
  "title": "Scalability in Perception for Autonomous Driving: Waymo Open Dataset",
  "first_author": "Pei Sun",
  "date": "2019-12"
 },
 "1903.11027": {
  "short": "nuScenes",
  "title": "nuScenes: A multimodal dataset for autonomous driving",
  "first_author": "Holger Caesar",
  "date": "2019-03"
 },
 "2406.15349": {
  "short": "NAVSIM",
  "title": "NAVSIM: Data-Driven Non-Reactive Autonomous Vehicle Simulation and Benchmarking",
  "first_author": "Daniel Dauner",
  "date": "2024-06"
 },
 "2406.03877": {
  "short": "Bench2Drive",
  "title": "Bench2Drive: Towards Multi-Ability Benchmarking of Closed-Loop End-To-End Autonomous Driving",
  "first_author": "Xiaosong Jia",
  "date": "2024-06"
 },
 "1711.03938": {
  "short": "CARLA",
  "title": "CARLA: An Open Urban Driving Simulator",
  "first_author": "Alexey Dosovitskiy",
  "date": "2017-11"
 },
 "2606.03159": {
  "short": "OmniDreams",
  "title": "NVIDIA OmniDreams: Real-Time Generative World Model for Closed-Loop Autonomous Vehicle Simulation",
  "first_author": " NVIDIA",
  "date": "2026-06"
 },
 "2511.00088": {
  "short": "Alpamayo-R1",
  "title": "Alpamayo-R1: Bridging Reasoning and Action Prediction for Generalizable Autonomous Driving in the Long Tail",
  "first_author": " NVIDIA",
  "date": "2025-10"
 },
 "2404.09432": {
  "short": "8th AI City Challenge",
  "title": "The 8th AI City Challenge",
  "first_author": "Shuo Wang",
  "date": "2024-04"
 },
 "2508.13564": {
  "short": "9th AI City Challenge",
  "title": "The 9th AI City Challenge",
  "first_author": "Zheng Tang",
  "date": "2025-08"
 },
 "2412.00692": {
  "short": "MCBLT",
  "title": "MCBLT: Multi-Camera Multi-Object 3D Tracking in Long Videos",
  "first_author": "Yizhou Wang",
  "date": "2024-12"
 },
 "2009.07736": {
  "short": "HOTA",
  "title": "HOTA: A Higher Order Metric for Evaluating Multi-Object Tracking",
  "first_author": "Jonathon Luiten",
  "date": "2020-09"
 },
 "2507.10778": {
  "short": "AI City 2025 Track 3 winner",
  "title": "Warehouse Spatial Question Answering with LLM Agent",
  "first_author": "Hsiang-Wei Huang",
  "date": "2025-07"
 },
 "2509.15490": {
  "short": "SmolRGPT",
  "title": "SmolRGPT: Efficient Spatial Reasoning for Warehouse Environments with 600M Parameters",
  "first_author": "Abdarahmane Traore",
  "date": "2025-09"
 },
 "2310.17274": {
  "short": "cuRobo",
  "title": "cuRobo: Parallelized Collision-Free Minimum-Jerk Robot Motion Generation",
  "first_author": "Balakumar Sundaralingam",
  "date": "2023-10"
 },
 "1802.08705": {
  "short": "PDDLStream",
  "title": "PDDLStream: Integrating Symbolic Planners and Blackbox Samplers via Optimistic Adaptive Planning",
  "first_author": "Caelan Reed Garrett",
  "date": "2018-02"
 },
 "2509.20297": {
  "short": "mindmap",
  "title": "mindmap: Spatial Memory in Deep Feature Maps for 3D Action Policies",
  "first_author": "Remo Steiner",
  "date": "2025-09"
 },
 "2606.05160": {
  "short": "GRAIL",
  "title": "GRAIL: Generating Humanoid Loco-Manipulation from 3D Assets and Video Priors",
  "first_author": "Tianyi Xie",
  "date": "2026-06"
 },
 "2511.07820": {
  "short": "SONIC",
  "title": "SONIC: Supersizing Motion Tracking for Natural Humanoid Whole-Body Control",
  "first_author": "Zhengyi Luo",
  "date": "2025-11"
 },
 "2410.17491": {
  "short": "X-MOBILITY",
  "title": "X-MOBILITY: End-To-End Generalizable Navigation via World Modeling",
  "first_author": "Wei Liu",
  "date": "2024-10"
 },
 "2507.13097": {
  "short": "GraspGen",
  "title": "GraspGen: A Diffusion-based Framework for 6-DOF Grasping with On-Generator Training",
  "first_author": "Adithyavairavan Murali",
  "date": "2025-07"
 },
 "2406.11793": {
  "short": "FetchBench",
  "title": "FetchBench: A Simulation Benchmark for Robot Fetching",
  "first_author": "Beining Han",
  "date": "2024-06"
 },
 "2011.09584": {
  "short": "ACRONYM",
  "title": "ACRONYM: A Large-Scale Grasp Dataset Based on Simulation",
  "first_author": "Clemens Eppner",
  "date": "2020-11"
 },
 "2509.19296": {
  "short": "Lyra",
  "title": "Lyra: Generative 3D Scene Reconstruction via Video Diffusion Model Self-Distillation",
  "first_author": "Sherwin Bahmani",
  "date": "2025-09"
 },
 "2503.03751": {
  "short": "GEN3C",
  "title": "GEN3C: 3D-Informed World-Consistent Video Generation with Precise Camera Control",
  "first_author": "Xuanchi Ren",
  "date": "2025-03"
 },
 "2508.10934": {
  "short": "ViPE",
  "title": "ViPE: Video Pose Engine for 3D Geometric Perception",
  "first_author": "Jiahui Huang",
  "date": "2025-08"
 },
 "2602.15922": {
  "short": "DreamZero",
  "title": "World Action Models are Zero-shot Policies",
  "first_author": "Seonghyeon Ye",
  "date": "2026-02"
 },
 "2505.12705": {
  "short": "DreamGen",
  "title": "DreamGen: Unlocking Generalization in Robot Learning through Video World Models",
  "first_author": "Joel Jang",
  "date": "2025-05"
 },
 "2602.24096": {
  "short": "DiffusionHarmonizer",
  "title": "DiffusionHarmonizer: Bridging Neural Reconstruction and Photorealistic Simulation with Online Diffusion Enhancer",
  "first_author": "Yuxuan Zhang",
  "date": "2026-02"
 },
 "2609.09396": {
  "short": "VANTAGE-Bench",
  "title": "VANTAGE-Bench: Evaluating the Infrastructure AI Gap in Vision-Language Models",
  "first_author": "Zaid Pervaiz Bhat",
  "date": "2026-09"
 },
 "2502.00392": {
  "short": "RefDrone",
  "title": "RefDrone: A Challenging Benchmark for Referring Expression Comprehension in Drone Scenes",
  "first_author": "Zhichao Sun",
  "date": "2025-02"
 },
 "2505.19877": {
  "short": "Vad-R1",
  "title": "Vad-R1: Towards Video Anomaly Reasoning via Perception-to-Cognition Chain-of-Thought",
  "first_author": "Chao Huang",
  "date": "2025-05"
 },
 "2212.09258": {
  "short": "CHAD",
  "title": "CHAD: Charlotte Anomaly Dataset",
  "first_author": "Armin Danesh Pazho",
  "date": "2022-12"
 },
 "2608.10317": {
  "short": "TAR-Bench",
  "title": "From Detection to Understanding: TAR and TAR-Bench for Multi-Task Traffic Anomaly Reasoning",
  "first_author": "Han Zhang",
  "date": "2026-08"
 },
 "2602.09153": {
  "short": "SceneSmith",
  "title": "SceneSmith: Agentic Generation of Simulation-Ready Indoor Scenes",
  "first_author": "Nicholas Pfaff",
  "date": "2026-02"
 },
 "2607.00033": {
  "short": "CHORD (V2D tech report)",
  "title": "Learning Dexterous Manipulation Using Contact Wrench Guidance From Human Demonstration",
  "first_author": "Xinghao Zhu",
  "date": "2026-06"
 },
 "2602.10116": {
  "short": "SAGE",
  "title": "SAGE: Scalable Agentic 3D Scene Generation for Embodied AI",
  "first_author": "Hongchi Xia",
  "date": "2026-02"
 },
 "2203.11089": {
  "short": "OpenLane (PersFormer)",
  "title": "PersFormer: 3D Lane Detection via Perspective Transformer and the OpenLane Benchmark",
  "first_author": "Li Chen",
  "date": "2022-03"
 },
 "1805.09817": {
  "short": "RealEstate10K (Stereo Magnification)",
  "title": "Stereo Magnification: Learning View Synthesis using Multiplane Images",
  "first_author": "Tinghui Zhou",
  "date": "2018-05"
 },
 "2312.16256": {
  "short": "DL3DV-10K",
  "title": "DL3DV-10K: A Large-Scale Scene Dataset for Deep Learning-based 3D Vision",
  "first_author": "Lu Ling",
  "date": "2023-12"
 }
}

ROWS = {
 "PhysicalAI-Robotics-GR00T-X-Embodiment-Sim": {
  "papers": [
   "2503.14734",
   "2410.24185",
   "2406.02523"
  ],
  "benchmarks": [
   "2406.02523",
   "2410.24185",
   "2503.14734"
  ],
  "benchmarks_other": "",
  "note": "Card groups: cross-embodied bimanual 9k (DexMimicGen suite, 9 tasks), GR1 tabletop 240k (RoboCasa framework, 24 tasks), robot-arm kitchen 72k (RoboCasa Kitchen, 24 tasks), G1 loco-manipulation 102. These are exactly the GR00T N1 simulation benchmarks."
 },
 "PhysicalAI-Robotics-GR00T-Teleop-Sim": {
  "papers": [
   "2503.14734"
  ],
  "benchmarks": [
   "2503.14734"
  ],
  "benchmarks_other": "",
  "note": "GR-1 tabletop simulation tasks from the GR00T N1 paper (RoboCasa framework)."
 },
 "PhysicalAI-WorldModel-Synthetic-Autonomous-Driving-Scenarios": {
  "papers": [
   "2606.02800"
  ],
  "benchmarks": [
   "2512.01989",
   "2501.09038",
   "2406.15349",
   "2406.03877"
  ],
  "benchmarks_other": "PBench (nvidia/PBench, no arXiv); Cosmos-HumanEval HUE (nvidia/Cosmos-HumanEval-v1, no arXiv)",
  "note": "Released as SDG-DriveSim (Cosmos 3 report, Appendix C.3); used in Cosmos 3 midtraining. World-model quality: PAI-Bench, Physics-IQ, PBench; AV closed-loop: NAVSIM, Bench2Drive."
 },
 "PhysicalAI-WorldModel-Synthetic-Physical-Interaction-Scenes": {
  "papers": [
   "2606.02800",
   "2606.03551"
  ],
  "benchmarks": [
   "2512.01989",
   "2501.09038",
   "2601.21282",
   "2410.05363",
   "2507.13428"
  ],
  "benchmarks_other": "PBench (no arXiv)",
  "note": "Released as SDG-PhyxSim (Cosmos 3, Appendix C.1). Physics-understanding benchmarks for world models."
 },
 "PhysicalAI-WorldModel-Synthetic-Warehouse-Operations-Scenes": {
  "papers": [
   "2606.02800",
   "2606.03551"
  ],
  "benchmarks": [
   "2512.01989",
   "2501.09038",
   "2508.13564"
  ],
  "benchmarks_other": "PBench (no arXiv)",
  "note": "Released as SDG-Warehouse (Cosmos 3, Appendix C.5). Card positions it as a controlled robustness benchmark; smart-space perception benchmarks come from the AI City Challenge."
 },
 "PhysicalAI-WorldModel-Synthetic-Embodied-Robot-Scenes": {
  "papers": [
   "2606.02800",
   "2602.15922",
   "2310.17596",
   "2602.10116"
  ],
  "benchmarks": [
   "2506.18123",
   "2306.03310",
   "2406.02523",
   "2512.01989",
   "2501.09038"
  ],
  "benchmarks_other": "PolaRiS, Genie Sim 3.0 (no arXiv); PBench",
  "note": "Released as SDG-RobotSim (Cosmos 3, Appendix C.2); includes MimicGen and DreamZero manipulation clips and SOMA-retargeted motion in SAGE scenes. Cosmos 3 policy ranked first on RoboArena; DreamZero also reports PolaRiS and Genie Sim 3.0 (no arXiv)."
 },
 "PhysicalAI-WorldModel-Synthetic-Digital-Human-Scenes": {
  "papers": [
   "2606.02800",
   "2602.09153"
  ],
  "benchmarks": [
   "2512.01989",
   "2501.09038"
  ],
  "benchmarks_other": "Human World Bench and PBench (Cosmos 3 report, no separate arXiv)",
  "note": "Released as SDG-SynHuman (Cosmos 3, Appendix C.4); indoor scenes from SceneSmith. Cosmos 3 reports Human World Bench (HWB) for human-centric generation."
 },
 "PhysicalAI-SmartSpaces": {
  "papers": [
   "2404.09432",
   "2508.13564",
   "2412.00692"
  ],
  "benchmarks": [
   "2404.09432",
   "2508.13564",
   "2009.07736"
  ],
  "benchmarks_other": "",
  "note": "AI City Challenge Track 1 (multi-camera 3D tracking) 2024, 2025, 2026 editions; scored with HOTA on the challenge evaluation server."
 },
 "PhysicalAI-Spatial-Intelligence-Warehouse": {
  "papers": [
   "2508.13564"
  ],
  "benchmarks": [
   "2508.13564",
   "2507.10778",
   "2509.15490"
  ],
  "benchmarks_other": "",
  "note": "AI City Challenge 2025 Track 3 (Warehouse Spatial Intelligence); winning solution and SmolRGPT report accuracy on its test split."
 },
 "PhysicalAI-Robotics-Manipulation-SingleArm": {
  "papers": [
   "2310.17274",
   "1802.08705",
   "2606.03551"
  ],
  "benchmarks": [],
  "benchmarks_other": "scene_synthesizer (JOSS)",
  "note": "Generated with cuRobo + PDDLStream planning in scene_synthesizer scenes (JOSS 10.21105/joss.07561, no arXiv). No public benchmark named on the card."
 },
 "PhysicalAI-Robotics-Manipulation-Kitchen": {
  "papers": [
   "2310.17274",
   "1802.08705",
   "2606.03551"
  ],
  "benchmarks": [],
  "benchmarks_other": "scene_synthesizer (JOSS)",
  "note": "Same pipeline as SingleArm; no public benchmark named on the card."
 },
 "PhysicalAI-Robotics-Manipulation-Objects": {
  "papers": [
   "2310.17274",
   "1802.08705",
   "2606.03551"
  ],
  "benchmarks": [],
  "benchmarks_other": "scene_synthesizer (JOSS)",
  "note": "Same pipeline as SingleArm; no public benchmark named on the card."
 },
 "PhysicalAI-Robotics-Manipulation-Augmented": {
  "papers": [
   "2310.17596",
   "2503.14492",
   "2511.04831"
  ],
  "benchmarks": [],
  "benchmarks_other": "",
  "note": "Franka cube-stacking demos (Isaac Lab Mimic) with Cosmos-Transfer1 augmentation; no public benchmark named."
 },
 "PhysicalAI-GR00T-Tuned-Tasks": {
  "papers": [
   "2310.17596",
   "2511.04831",
   "2503.14734"
  ],
  "benchmarks": [
   "2503.14734"
  ],
  "benchmarks_other": "",
  "note": "MimicGen demos for GR1 industrial tabletop tasks; evaluated in the GR00T N1 style sim suites."
 },
 "Arena-G1-Loco-Manipulation-Task": {
  "papers": [
   "2511.04831",
   "2310.17596"
  ],
  "benchmarks": [],
  "benchmarks_other": "Isaac Lab-Arena policy evaluation (GitHub isaac-sim/IsaacLab-Arena)",
  "note": "Isaac Lab-Arena environment (Isaac Lab paper Sec. 7.2.1); Arena is the evaluation harness itself, no separate arXiv."
 },
 "Arena-G1-Static-PickNPlace-Task": {
  "papers": [
   "2511.04831"
  ],
  "benchmarks": [],
  "benchmarks_other": "Isaac Lab-Arena policy evaluation (GitHub)",
  "note": "Isaac Lab-Arena environment."
 },
 "Arena-GR1-Manipulation-Task": {
  "papers": [
   "2511.04831",
   "2310.17596"
  ],
  "benchmarks": [],
  "benchmarks_other": "Isaac Lab-Arena policy evaluation (GitHub)",
  "note": "Isaac Lab-Arena environment with MimicGen demos."
 },
 "Arena-GR1-Manipulation-PlaceItemCloseDoor-Task": {
  "papers": [
   "2511.04831",
   "2310.17596"
  ],
  "benchmarks": [],
  "benchmarks_other": "Isaac Lab-Arena policy evaluation (GitHub)",
  "note": "Isaac Lab-Arena environment with MimicGen demos."
 },
 "Arena-GR1-Manipulation-Task-v3": {
  "papers": [
   "2511.04831"
  ],
  "benchmarks": [],
  "benchmarks_other": "Isaac Lab-Arena policy evaluation (GitHub)",
  "note": "LeRobot v3 export of an Arena task."
 },
 "Arena-DROID-Camera-Sensitivity-Workflow-Sample": {
  "papers": [
   "2511.04831",
   "2403.12945"
  ],
  "benchmarks": [
   "2403.12945"
  ],
  "benchmarks_other": "Isaac Lab-Arena DROID evaluation workflow (GitHub)",
  "note": "Camera-sensitivity analysis of a DROID-trained policy inside Isaac Lab-Arena."
 },
 "PhysicalAI-Robotics-mindmap-Franka-Cube-Stacking": {
  "papers": [
   "2509.20297",
   "2310.17596",
   "2511.04831"
  ],
  "benchmarks": [
   "2509.20297"
  ],
  "benchmarks_other": "",
  "note": "mindmap's own Isaac Lab spatial-memory task suite (4 tasks, 100 randomizations each); paper rejects RLBench as unsuitable."
 },
 "PhysicalAI-Robotics-mindmap-Franka-Mug-in-Drawer": {
  "papers": [
   "2509.20297",
   "2310.17596",
   "2511.04831"
  ],
  "benchmarks": [
   "2509.20297"
  ],
  "benchmarks_other": "",
  "note": "mindmap task suite."
 },
 "PhysicalAI-Robotics-mindmap-GR1-Drill-in-Box": {
  "papers": [
   "2509.20297",
   "2310.17596",
   "2511.04831"
  ],
  "benchmarks": [
   "2509.20297"
  ],
  "benchmarks_other": "",
  "note": "mindmap task suite."
 },
 "PhysicalAI-Robotics-mindmap-GR1-Stick-in-Bin": {
  "papers": [
   "2509.20297",
   "2310.17596",
   "2511.04831"
  ],
  "benchmarks": [
   "2509.20297"
  ],
  "benchmarks_other": "",
  "note": "mindmap task suite."
 },
 "g1_locomanip_dataset": {
  "papers": [
   "2511.04831"
  ],
  "benchmarks": [],
  "benchmarks_other": "",
  "note": "Isaac Lab loco-manipulation data generation (Isaac Lab paper Sec. 5.5.1); demonstration artifact, no benchmark."
 },
 "PhysicalAI-Robotics-Locomanipulation-GRAIL": {
  "papers": [
   "2606.05160",
   "2511.07820",
   "2406.02523",
   "2511.04831"
  ],
  "benchmarks": [
   "2606.05160"
  ],
  "benchmarks_other": "",
  "note": "GRAIL reports its own pick-up, whole-body manipulation and terrain-traversal evaluations (real Unitree G1); RoboCasa supplies assets."
 },
 "X-Mobility": {
  "papers": [
   "2410.17491",
   "2606.03551"
  ],
  "benchmarks": [
   "2410.17491"
  ],
  "benchmarks_other": "",
  "note": "Custom closed-loop Isaac Sim warehouse benchmark (10 scenarios, 5 held out) plus 50 random cluttered corridors; Nav2 and MILE baselines."
 },
 "PhysicalAI-Autonomous-Vehicles-NuRec": {
  "papers": [
   "2412.12507",
   "2407.07090",
   "2607.14203",
   "2606.03159",
   "2511.00088"
  ],
  "benchmarks": [
   "1912.04838",
   "2406.15349",
   "2406.03877",
   "1711.03938"
  ],
  "benchmarks_other": "NuRec-AV-Object-Benchmark (nvidia HF, no arXiv)",
  "note": "NuRec renders in 3DGUT; CARLA integration on the card enables closed-loop use. Instant NuRec evaluates reconstruction on Waymo Open. NAVSIM and Bench2Drive are the standard closed-loop AV benchmarks."
 },
 "PhysicalAI-Robotics-NuRec": {
  "papers": [
   "2412.12507",
   "2407.07090",
   "2606.03551"
  ],
  "benchmarks": [],
  "benchmarks_other": "TUM RGB-D benchmark (IROS 2012)",
  "note": "3DGUT scenes for Isaac Sim; trajectories in TUM RGB-D format (Sturm et al. 2012, no arXiv). No benchmark named."
 },
 "PhysicalAI-Autonomous-Vehicle-Cosmos-Drive-Dreams": {
  "papers": [
   "2506.09042",
   "2503.14492",
   "2501.03575"
  ],
  "benchmarks": [
   "1912.04838",
   "2203.11089"
  ],
  "benchmarks_other": "",
  "note": "Paper evaluates 3D lane detection and 3D object detection on Waymo Open (with OpenLane corner-case splits) and policy learning on internal RDS-Bench."
 },
 "PhysicalAI-Autonomous-Vehicle-Cosmos-Synthetic": {
  "papers": [
   "2506.09042"
  ],
  "benchmarks": [
   "1912.04838",
   "2203.11089"
  ],
  "benchmarks_other": "",
  "note": "Alias of Cosmos-Drive-Dreams."
 },
 "PhysicalAI-SpatialIntelligence-Lyra-SDG": {
  "papers": [
   "2509.19296",
   "2503.03751",
   "2508.10934"
  ],
  "benchmarks": [
   "1805.09817",
   "2312.16256"
  ],
  "benchmarks_other": "Tanks and Temples",
  "note": "Lyra evaluates single-image-to-3D on RealEstate10K, DL3DV and Tanks and Temples (no arXiv, ACM TOG 2017)."
 },
 "PhysicalAI-Event-Videos": {
  "papers": [
   "2606.02800",
   "2505.19877",
   "2212.09258"
  ],
  "benchmarks": [
   "2505.19877",
   "2212.09258",
   "2608.10317"
  ],
  "benchmarks_other": "",
  "note": "Generated with Veo 3 and Cosmos 3 Super; annotation index also covers CHAD and Vad-R1 media. TAR-Bench is the sibling NVIDIA traffic-anomaly benchmark (AI City 2026 Track 3)."
 },
 "Harmonizer-Dataset": {
  "papers": [
   "2602.24096",
   "2412.12507"
  ],
  "benchmarks": [],
  "benchmarks_other": "",
  "note": "DiffusionHarmonizer (CVPR 2026) reports a user study; no public benchmark."
 },
 "PhysicalAI-VANTAGE-Bench": {
  "papers": [
   "2609.09396"
  ],
  "benchmarks": [
   "2609.09396",
   "2502.00392"
  ],
  "benchmarks_other": "",
  "note": "Is itself a benchmark: 8 tasks, 3,346 media assets, 17 models evaluated, leaderboard at vantage-bench.org; cites RefDrone."
 },
 "PhysicalAI-VANTAGE-Bench-Subset": {
  "papers": [
   "2609.09396"
  ],
  "benchmarks": [
   "2609.09396"
  ],
  "benchmarks_other": "",
  "note": "Subset of VANTAGE-Bench; annotations held server-side."
 },
 "video-to-data-robot-dexterity-task-library-and-dataset": {
  "papers": [
   "2607.00033",
   "2511.04831"
  ],
  "benchmarks": [
   "2607.00033"
  ],
  "benchmarks_other": "",
  "note": "V2D tech report (CHORD) introduces a 4,739-task bimanual dexterous simulation benchmark; 1,831 tasks evaluated. Companion nvidia/video_to_data_challenge on HF."
 },
 "PhysicalAI-Robotics-GraspGen": {
  "papers": [
   "2507.13097",
   "2011.09584"
  ],
  "benchmarks": [
   "2406.11793",
   "2011.09584"
  ],
  "benchmarks_other": "",
  "note": "GraspGen labels grasps in Isaac Sim (PhysX) and reports state of the art on FetchBench; ACRONYM is the baseline dataset."
 }
}

DOMAIN = [
 [
  "Robot manipulation, simulation",
  [
   "2306.03310",
   "2406.02523",
   "2405.05941",
   "2410.24185",
   "2403.09227",
   "2112.03227",
   "2410.00425",
   "2009.12293"
  ]
 ],
 [
  "Robot policies, real-world and datasets",
  [
   "2506.18123",
   "2403.12945",
   "2310.08864"
  ]
 ],
 [
  "Autonomous driving",
  [
   "1903.11027",
   "1912.04838",
   "2406.15349",
   "2406.03877",
   "1711.03938",
   "2203.11089"
  ]
 ],
 [
  "World models and video generation",
  [
   "2311.17982",
   "2501.09038",
   "2502.20694",
   "2410.05363",
   "2507.13428",
   "2601.21282",
   "2512.01989"
  ]
 ],
 [
  "Smart spaces and infrastructure video",
  [
   "2404.09432",
   "2508.13564",
   "2009.07736",
   "2609.09396"
  ]
 ],
 [
  "Grasping and 3D reconstruction",
  [
   "2406.11793",
   "2011.09584",
   "1805.09817",
   "2312.16256"
  ]
 ]
]
