> [!abstract] ASSISTANT
> Session initialized. Live session is now linked to Representation Learning.md.


> [!question] Phase 1a — Probe Current Level
> 1a. Current Level Probe: Before we dive into the lecture material on Representation Learning, Embeddings, and Contrastive Losses, which statement best captures your current familiarity with how neural network layers transform data into latent spaces?
>
> 1. I know basic machine learning / neural networks, but I haven't looked closely at how specific layers (like L2 normalization or ReLU) reshape input spaces geometrically or how contrastive loss functions operate.
> 2. I understand standard feature vectors and basic autoencoders (encoder-decoder architectures), but concepts like L2 norm mapping data onto a unit hypersphere, softmax line constraints, or triplet loss margin tuning are new or rusty for me.
> 3. I am already very comfortable with geometric layer transformations, autoencoders, L2 norm unit hypersphere mappings, triplet losses, and hard/semi-hard negative mining.


> [!question] Phase 1b — Probe Learning Goal
> 1b. Learning Goal: Since we are replicating your instructor's lecture on 'Session 5 — Embeddings & Image Similarity', what style and depth would you like for this session?
>
> 1. (Recommended) Full classroom lecture experience — Walk me through step-by-step with the instructor's exact tone, Socratic questions, intuition checks, math derivations, and DAG dependency maps.
> 2. Fast-paced deep dive — Focus primarily on the core mathematical derivations, loss functions (triplet, contrastive, self-supervised pre-text tasks), and key geometric intuitions.
> 3. Comprehensive concept-by-concept walkthrough — Cover all concepts systematically with extra focus on intuitive visual analogies and practical real-world applications.


> [!example] Answer
> 1. I know basic machine learning / neural networks, but I haven't looked closely at how specific layers (like L2 normalization or ReLU) reshape input spaces geometrically or how contrastive loss functions operate.
> Combination of full classroom lecture & comprehensive concept walkthrough with strong emphasis on VISUAL representations.


> [!note] Research Findings (Lecture Content Verified)
> ### Verified Research Findings from Session 5 (Embeddings & Image Similarity)
>
> 1. **Foundational Definitions**:
>    - **Forward Mapping (Representation Learning)**: : \mathcal{X} 
ightarrow \mathbb{R}^d$ maps input points  \mapsto z$.
>    - **Reverse Mapping (Generative Modeling)**: : \mathbb{R}^d 
ightarrow \mathcal{X}$ reconstructs inputs  \mapsto \hat{x}$.
>    - **Good Representation Properties**: Compactness ( \ll 	ext{dim}(\mathcal{X})$), Explanatoriness, Disentanglement, Interpretability, and Downstream Transferability.
>
> 2. **Layer-by-Layer Geometric Transformations**:
>    - **Linear Layer ( x + b$)**: Affine transformation (scaling, rotation, translation).
>    - **ReLU ($\max(0, x)$)**: Quadrant folding — maps all negative coordinates to 0, restricting activations to the non-negative hyper-octant ( \ge 0$).
>    - **L2 Normalization ( / ||x||_2$)**: Hypersphere projection — constrains 2D vectors onto a unit circle (^2 + x_2^2 = 1$) or hBcdimensional hypersphere $\mathbb{S}^{d-1}$.
>    - **Softmax ($\exp(x_i)/\sum \exp(x_k)$)**: Simplex mapping — constrains logits onto a probability hyperplane where $\sum x_i = 1$.
>
> 3. **Taxonomy & Self-Supervised Pretext Tasks**:
>    - **Supervised vs Unsupervised vs Metric Learning vs Self-Supervised**.
>    - **CIE *a*b*$ Colorization**: Input grayscale  \in \mathbb{R}^{H 	imes W 	imes 1}$, predict color channels  \in \mathbb{R}^{H 	imes W 	imes 2}$.
>    - **ADAS Temporal Depth Estimation**: Reconstruct frame +1$ from frame $ via 3D reprojection error.
>    - **Masked Autoencoders (MAE)**: 75%+ patch masking for images vs 15% token masking in BERT MLM.
>
> 4. **Metric Learning & Contrastive Loss**:
>    - **Cosine Similarity**: $	ext{sim}(u, v) = rac{u^	op v}{||u||_2 ||v||_2}$.
>    - **Triplet Loss**: $\mathcal{L}_{	ext{triplet}}(x_a, x_p, x_n) = \max(0, ||f(x_a) - f(x_p)||_2^2 - ||f(x_a) - f(x_n)||_2^2 + \epsilon)$.
>    - **Negative Mining**: Hard ((a,n) < d(a,p)$), Semi-Hard ((a,p) < d(a,n) < d(a,p) + \epsilon$), Easy ((a,n) > d(a,p) + \epsilon$).


> [!tip] Phase 2 — Proposed Lesson Plan & DAG
> ### Session Teaching Plan: Session 5 — Representation Learning & Embeddings
>
> **Approach**:
> We will deliver this class imitating your instructor's authentic classroom style — starting from unconditional geometric first-principles, progressing through motivated discoveries, and checking understanding Socratically at each node. To cater to your visual learning preference, every key transformation (ReLU folding, L2 circle projection, Softmax simplex, Triplet Loss margin boundaries) will feature explicit geometric visual representations and LaTeX math formatting.
>
> **Dependency Map (DAG)**:
>


> [!note] Research Findings (Lecture Content Verified)
> ### Verified Research Findings from Session 5 (Embeddings & Image Similarity)
>
> 1. **Foundational Definitions**:
>    - **Forward Mapping (Representation Learning)**: $f: \mathcal{X} \rightarrow \mathbb{R}^d$ maps input points $x \mapsto z$.
>    - **Reverse Mapping (Generative Modeling)**: $g: \mathbb{R}^d \rightarrow \mathcal{X}$ reconstructs inputs $z \mapsto \hat{x}$.
>    - **Good Representation Properties**: Compactness ($d \ll \text{dim}(\mathcal{X})$), Explanatoriness, Disentanglement, Interpretability, and Downstream Transferability.
>
> 2. **Layer-by-Layer Geometric Transformations**:
>    - **Linear Layer ($W x + b$)**: Affine transformation (scaling, rotation, translation).
>    - **ReLU ($\\max(0, x)$)**: Quadrant folding — maps all negative coordinates to 0, restricting activations to the non-negative hyper-octant ($x \ge 0$).
>    - **L2 Normalization ($x / ||x||_2$)**: Hypersphere projection — constrains 2D vectors onto a unit circle ($x_1^2 + x_2^2 = 1$) or $d$-dimensional hypersphere $\mathbb{S}^{d-1}$.
>    - **Softmax ($\\exp(x_i)/\\sum \\exp(x_k)$)**: Simplex mapping — constrains logits onto a probability hyperplane where $\\sum x_i = 1$.
>
> 3. **Taxonomy & Self-Supervised Pretext Tasks**:
>    - **Supervised vs Unsupervised vs Metric Learning vs Self-Supervised**.
>    - **CIE $L*a*b*$ Colorization**: Input grayscale $L \in \mathbb{R}^{H \times W \times 1}$, predict color channels $ab \in \mathbb{R}^{H \times W \times 2}$.
>    - **ADAS Temporal Depth Estimation**: Reconstruct frame $t+1$ from frame $t$ via 3D reprojection error.
>    - **Masked Autoencoders (MAE)**: 75%+ patch masking for images vs 15% token masking in BERT MLM.
>
> 4. **Metric Learning & Contrastive Loss**:
>    - **Cosine Similarity**: $\text{sim}(u, v) = \frac{u^\top v}{||u||_2 ||v||_2}$.
>    - **Triplet Loss**: $\mathcal{L}_{\text{triplet}}(x_a, x_p, x_n) = \max(0, ||f(x_a) - f(x_p)||_2^2 - ||f(x_a) - f(x_n)||_2^2 + \epsilon)$.
>    - **Negative Mining**: Hard ($d(a,n) < d(a,p)$), Semi-Hard ($d(a,p) < d(a,n) < d(a,p) + \epsilon$), Easy ($d(a,n) > d(a,p) + \epsilon$).


> [!tip] Phase 2 — Proposed Lesson Plan & DAG
> ### Session Teaching Plan: Session 5 — Representation Learning & Embeddings
>
> **Approach**:
> We will deliver this class imitating your instructor's authentic classroom style — starting from unconditional geometric first-principles, progressing through motivated discoveries, and checking understanding Socratically at each node. To cater to your visual learning preference, every key transformation (ReLU folding, L2 circle projection, Softmax simplex, Triplet Loss margin boundaries) will feature explicit geometric visual representations and LaTeX math formatting.
>
> **Dependency Map (DAG)**:
>
> ```mermaid
> flowchart TD
>     N1["Node 1: Forward Encoder Mapping<br/>(f: X -> R^d & Vector Embeddings)"] --> N2["Node 2: Layer-by-Layer Geometric Transformations<br/>(Linear, ReLU, L2 Norm, Softmax)"]
>     N2 --> N3["Node 3: Representation Learning Taxonomy & Autoencoders<br/>(Supervised vs Unsupervised vs Metric vs Self-Supervised)"]
>     N3 --> N4["Node 4: Self-Supervised Pretext Tasks<br/>(L*a*b Colorization, ADAS Temporal Depth, Masked Modeling)"]
>     N4 --> N5["Node 5: Distance Metrics & Contrastive Losses<br/>(Cosine Similarity, Triplet Loss & Negative Mining)"]
> ```


> [!abstract] Node 1 — Forward Encoder Mapping & Vector Embeddings
> ## Node 1: Forward Encoder Mapping ($f: \mathcal{X} \rightarrow \mathbb{R}^d$) & Vector Embeddings
>
> ### 1. Motivation: Why learn representations?
> Think about how your brain processes visual scenes in the real world. Suppose I show you an image containing a car parked in front of a house, and I ask: *"Where is the car?"* 
>
> Do you evaluate all $28 \times 28 = 784$ (or $1024 \times 1024 \times 3 \approx 3.1$ million) pixel intensity values individually? **No!** Your visual cortex immediately isolates the car from the background, discarding millions of irrelevant pixel details (like cloud patterns or brick textures) and focusing purely on the compact entity needed for the task.
>
> In computer vision and machine learning, raw input data space $\mathcal{X}$ is incredibly dense, complex, and noisy. We want the computer to learn a **compact representation** $z$ that compresses this massive pixel space into a vector containing only the essential semantic information.
>
> ```
> [ Raw Image x ∈ X ]  ───( Encoder f )───►  [ Feature Vector z ∈ R^d ]
>  (High-dim: 1024x1024x3)                       (Compressed: d = 128 or 512)
> ```
>
> ---
>
> ### 2. Establishing Unconditional First-Principles
>
> #### **A. Representation Learning vs. Generative Modeling**
> Every deep learning architecture operating on data handles mapping between two primary spaces:
>
> 1. **Forward Mapping (Representation Learning)**:
>    An **Encoder** is a parameterised function $f: \mathcal{X} \rightarrow \mathbb{R}^d$ that maps raw observed data points $x \in \mathcal{X}$ into a low-dimensional latent space $\mathbb{R}^d$:
>    $$z = f(x), \quad \text{where } z \in \mathbb{R}^d \text{ and } d \ll \text{dim}(\mathcal{X})$$
>
> 2. **Reverse Mapping (Generative Modeling)**:
>    A **Decoder** (or Generator) is a function $g: \mathbb{R}^d \rightarrow \mathcal{X}$ that maps latent vectors $z \in \mathbb{R}^d$ back into observed high-dimensional data space $\mathcal{X}$:
>    $$\hat{x} = g(z), \quad \text{where } \hat{x} \in \mathcal{X}$$
>    *(Examples: Autoencoder decoders reconstructing images, or LLM decoders mapping hidden token vectors back to natural language words).*
>
> ```mermaid
> flowchart LR
>     X["Observed Data Space X<br/>(e.g., Raw Pixels / Audio)"] -- "Forward Pass f(x)<br/>(Representation Learning)" --> Z["Latent Embedding Space R^d<br/>(Compact Vector z)"]
>     Z -- "Reverse Pass g(z)<br/>(Generative Modeling)" --> XHat["Reconstructed Data X̂"]
> ```
>
> #### **B. Properties of a "Good" Representation (Bengio et al.)**
> What makes a latent vector $z$ effective? We demand five core properties:
> 1. **Compactness**: $d \ll \text{dim}(\mathcal{X})$. Eliminates redundant pixels and high-frequency noise.
> 2. **Explanatoriness**: Retains sufficient signal required to solve target downstream tasks.
> 3. **Disentanglement**: Distinct physical factors of variation (e.g., shape, color, lighting) are isolated along independent axes in $\mathbb{R}^d$.
> 4. **Interpretability**: Human-analyzable or geometrically structured distributions in latent space.
> 5. **Transferability**: Features learned on Task A (e.g., ImageNet classification) easily transfer to Task B (e.g., medical image diagnosis) via transfer learning.
>
> ---
>
> ### 3. Connection
> This forward mapping $z = f(x)$ forms the foundational root ($N_1$) of our entire dependency graph. Every layer inside a neural network is simply a sequential step in building this transformation function $f(x)$. Next, in **Node 2**, we will look inside $f(x)$ to see how individual layer activations geometrically reshape data space.
>


> [!question] Node 1 Check — Concept Verification
> Node 1 Quiz Check: Suppose we have a network whose first stage takes a 512 x 512 x 3 image x and outputs a 128-dimensional vector z = f(x). A second stage takes z and outputs a reconstructed image x̂ = g(z). Which of the following correctly categorizes these two mapping functions?
>
> 1. f(x) is representation learning mapping X -> R^d, while g(z) is generative modeling mapping R^d -> X.
> 2. f(x) is generative modeling mapping X -> R^d, while g(z) is representation learning mapping R^d -> X.
> 3. Both f(x) and g(z) are representation learning functions mapping within data space X.
> 4. Both f(x) and g(z) are generative modeling functions operating strictly inside latent space R^d.


> [!success] Quiz — correct ✓
> Your answer: 1. f(x) is representation learning mapping X -> R^d, while g(z) is generative modeling mapping R^d -> X.
> Correct answer: 1
>
> Correct! f(x) maps high-dimensional input space X down to latent embedding vector z in R^d (Representation Learning). g(z) takes latent vector z and reconstructs raw data x̂ in X (Generative Modeling).


> [!abstract] Node 2 — Layer-by-Layer Geometric Transformations
> ## Node 2: Layer-by-Layer Geometric Transformations inside a Neural Network
>
> ### 1. Motivation: What actually happens to data as it passes through a Neural Network?
> Many people treat deep neural networks as "black boxes" that somehow learn features. But under the hood, a neural network is simply a pipeline of continuous geometric transformations. Each layer takes the feature space, warps it, folds it, projects it, or normalizes it.
>
> Understanding these geometric operations gives us full control over the latent representation space $\mathbb{R}^d$.
>
> ---
>
> ### 2. Establishing the Four Fundamental Geometric Layer Transformations
>
> #### **A. Linear Layer: Affine Transformation**
> The fundamental building block of a dense neuron is:
> $$x_{\text{out}} = W x_{\text{in}} + b$$
> - **Geometry**: This is an **affine transformation**. The weight matrix $W$ performs linear scaling, stretching, and rotation, while the bias vector $b$ shifts (translates) the space.
> - It changes vector orientation and magnitude, but keeps straight lines straight.
>
> ---
>
> #### **B. ReLU Activation: Quadrant Folding (Truncation)**
> The Rectified Linear Unit is defined as:
> $$x_{\text{out}}[i] = \max(0, x_{\text{in}}[i])$$
>
> - **Geometry**: In 2D, raw linear outputs can fall into any of the 4 quadrants (positive or negative). ReLU takes every point in the 2nd, 3rd, and 4th quadrants (where coordinates are negative) and **folds/collapses** them onto the axes or the origin $(0,0)$.
> - **Result**: The feature space is compressed entirely into the non-negative first quadrant (or hyper-octant in higher dimensions, $x \ge 0$). This creates a dense concentration of zero activations at the origin.
>
> ```
>        Raw Feature Space (Linear)              After ReLU Activation
>                y ▲                                     y ▲
>                  │                                       │
>      Quadrant 2  │  Quadrant 1               Quadrant 2  │  Quadrant 1
>      (-x, +y)    │  (+x, +y)                 (Collapsed) │  Unchanged
>    ──────────────┼──────────────► x       ───────────────┼──────────────► x
>      Quadrant 3  │  Quadrant 4               (Collapsed) │ (Collapsed)
>      (-x, -y)    │  (+x, -y)                             │
> ```
>
> ---
>
> #### **C. L2 Normalization Layer: Unit Hypersphere Projection**
> Given a 2D input vector $x_{\text{in}} = [x_1, x_2]^\top$, the L2 norm (magnitude) is $\|x_{\text{in}}\|_2 = \sqrt{x_1^2 + x_2^2}$. The L2 normalized output vector is:
> $$x_{\text{out}} = \frac{x_{\text{in}}}{\|x_{\text{in}}\|_2} = \left[ \frac{x_1}{\sqrt{x_1^2 + x_2^2}}, \frac{x_2}{\sqrt{x_1^2 + x_2^2}} \right]^\top$$
>
> **Mathematical Proof of the Circle Geometry**:
> Why do L2-normalized outputs always lie on a circle? Let's square the components of $x_{\text{out}}$ and sum them:
> $$(x_{\text{out}}[1])^2 + (x_{\text{out}}[2])^2 = \left(\frac{x_1}{\sqrt{x_1^2 + x_2^2}}\right)^2 + \left(\frac{x_2}{\sqrt{x_1^2 + x_2^2}}\right)^2 = \frac{x_1^2 + x_2^2}{x_1^2 + x_2^2} = 1$$
>
> Recall from geometry: $x_1^2 + x_2^2 = r^2$ is the equation of a circle of radius $r$. When $r = 1$, it is a **unit circle**!
> - **2D Input**: Maps all points onto the circumference of a 2D unit circle ($x_1^2 + x_2^2 = 1$).
> - **3D Input**: Maps all points onto the surface of a 3D unit sphere ($x_1^2 + x_2^2 + x_3^2 = 1$).
> - **$d$-Dimensional Input**: Maps all points onto a $d$-dimensional **unit hypersphere** $\mathbb{S}^{d-1}$.
>
> ```
>         Raw Inputs (Arbitrary Magnitudes)            After L2 Normalization
>                  y ▲                                         y ▲
>              •   │    •                                      │  • (All points lie
>                  │                                        ╭──┼──╮ on unit circle
>          •       │        •                               │  │  │ x₁² + x₂² = 1)
>      ────────────┼────────────► x                     ────┼──┼──┼────► x
>                  │                                        │  │  │
>            •     │    •                                   ╰──┼──╯
>                  │                                           │
> ```
>
> ---
>
> #### **D. Softmax Activation: Probability Simplex (Hyperplane Mapping)**
> For raw logit vectors, Softmax computes:
> $$P(y = i \mid x) = \frac{e^{x_i}}{\sum_{k=1}^K e^{x_k}}$$
>
> **Mathematical Proof of the Simplex Geometry**:
> Summing all probabilities:
> $$\sum_{i=1}^K x_{\text{out}}[i] = \sum_{i=1}^K \frac{e^{x_i}}{\sum_{k=1}^K e^{x_k}} = \frac{\sum_{i=1}^K e^{x_i}}{\sum_{k=1}^K e^{x_k}} = 1$$
>
> For $K = 2$ dimensions: $x_1 + x_2 = 1$. This is the standard equation of a **straight line** ($y = -x + 1$)!
> For $K > 2$ dimensions: $\sum x_i = 1$ forms a $(K-1)$-dimensional **probability simplex** (a flat hyperplane slice through space).
>
> ```
>    Softmax Geometry (2D Output): x₁ + x₂ = 1
>                 x₂ ▲
>                  1 ┼╲
>                    │ ╲
>                    │  ╲  (Softmax Output Line)
>                    │   ╲  x₁ + x₂ = 1
>                  0 ┴────┴───────► x₁
>                         1
> ```
>
> ---
>
> ### 3. Connection
> Notice how each operation constrains the geometry of our latent space:
> - **Linear**: Shifts and scales space linearly.
> - **ReLU**: Eliminates negative space (folds into 1st quadrant).
> - **L2 Norm**: Eliminates scale variations by projecting points onto a unit hypersphere surface.
> - **Softmax**: Converts activations into probability space constrained to a linear simplex hyperplane.
>
> Next, in **Node 3**, we will see how these geometric building blocks are combined to build **Autoencoders** and structure the taxonomy of Representation Learning.
>


> [!question] Node 2 Check — Geometric Concept Verification
> Node 2 Quiz Check: Suppose an intermediate layer applies L2 normalization to its 2D feature vector [x_1, x_2]^	op, while the final layer applies a 2D Softmax activation [p_1, p_2]^	op. Which geometric shapes describe the sets of points produced by these two layers?
>
> 1. The L2 normalization layer outputs points strictly on the unit circle (x_1^2 + x_2^2 = 1), while the Softmax layer outputs points strictly on the probability line (p_1 + p_2 = 1).
> 2. The L2 normalization layer outputs points strictly on the probability line (x_1 + x_2 = 1), while the Softmax layer outputs points strictly on the unit circle (p_1^2 + p_2^2 = 1).
> 3. Both layers output points constrained inside the non-negative hyper-octant without specific boundary geometric constraints.
> 4. Both layers output arbitrary affine-transformed vectors bounded between -1 and +1.


> [!success] Quiz — correct ✓
> Your answer: 1. The L2 normalization layer outputs points strictly on the unit circle (x_1^2 + x_2^2 = 1), while the Softmax layer outputs points strictly on the probability line (p_1 + p_2 = 1).
> Correct answer: 1
>
> Correct! L2 normalization divides vectors by their magnitude ||x||_2, projecting them onto a unit circle/hypersphere (x_1^2 + x_2^2 = 1). Softmax forces vector elements to sum to 1, constraining them to a linear simplex line/hyperplane (p_1 + p_2 = 1).


> [!abstract] Node 3 — Representation Learning Taxonomy & Autoencoders
> ## Node 3: Representation Learning Taxonomy & Autoencoders
>
> ### 1. Motivation: The High Cost of Manual Labeling
> In supervised learning, we rely on labeled dataset pairs $\{(x^{(i)}, y^{(i)})\}$. But manual human annotation is expensive, time-consuming, and unscalable for billions of images or text documents.
>
> Can a network learn rich, meaningful feature representations **without human labels**? 
> This leads us to the taxonomy of learning paradigms, centered around **Autoencoders** and **Compression**.
>
> ---
>
> ### 2. Establishing the Taxonomy of Representation Learning
>
> ```mermaid
> flowchart TD
>     Paradigms["Representation Learning Paradigms"]
>     Paradigms --> Supervised["Supervised Learning<br/>(Requires ground-truth labels y)"]
>     Paradigms --> Unsupervised["Unsupervised Learning<br/>(Only raw data x)"]
>     Paradigms --> Metric["Metric Learning<br/>(Enforces distance constraints)"]
>     
>     Unsupervised --> Autoencoders["Autoencoders & Compression<br/>(Reconstruction Loss L2)"]
>     Unsupervised --> Clustering["Clustering & Quantization<br/>(K-Means / Discrete Clusters)"]
>     Unsupervised --> SelfSupervised["Self-Supervised Pretext Tasks<br/>(Synthesizes labels from x)"]
> ```
>
> #### **A. Supervised Representation Learning**
> - Objective: Minimize target error $\mathcal{L}(f(x^{(i)}), y^{(i)})$.
> - Features $z$ are learned *implicitly* as an intermediate byproduct of performing classification or regression.
>
> #### **B. Unsupervised Autoencoders (Compression & Reconstruction)**
> An Autoencoder consists of two sub-networks trained end-to-end:
> 1. **Encoder** ($f: \mathcal{X} \rightarrow \mathbb{R}^m$): Compresses high-dimensional input $x \in \mathbb{R}^n$ into bottleneck embedding $z \in \mathbb{R}^m$.
> 2. **Decoder** ($g: \mathbb{R}^m \rightarrow \mathcal{X}$): Reconstructs original data $\hat{x} \in \mathbb{R}^n$ from latent vector $z$.
>
> **Reconstruction Loss (L2 Norm Error)**:
> $$\mathcal{L}_{\text{recon}}(x, \hat{x}) = \|x - \hat{x}\|_2^2 = \|x - g(f(x))\|_2^2$$
>
> ```
>    [ Input x ∈ R^n ] ──► ( Encoder f ) ──► [ Bottleneck z ∈ R^m ] ──► ( Decoder g ) ──► [ Reconstructed x̂ ∈ R^n ]
>                                                    ▲
>                                            m < n (Bottleneck)
> ```
>
> **Why does this work?**
> If the bottleneck dimension $m < n$, the network cannot simply memorize $x$ (it would run out of capacity!). It is forced to learn a compressed, generalized representation of the data distribution.
>
> *Instructor's Nuance Check (Dimension $m$ vs $n$)*:
> - **Usually**: $m < n$ (Dimensionality reduction / compression).
> - **Special Case ($m > n$)**: Overcomplete representations or Cryptographic Encoding. In cryptography, a short 4-digit PIN is expanded into a high-dimensional encrypted key ($m \gg n$) to make breaking it computationally intractable without the private key.
>
> #### **C. Clustering & Quantization**
> - Maps continuous feature representations $z \in \mathbb{R}^d$ into discrete category indices $k \in \{1, \dots, K\}$ (e.g., K-Means, Vector Quantization).
> - Groups semantically similar data points together in latent space based on spatial proximity.
>
> ---
>
> ### 3. Connection
> Now that we have established how Autoencoders use reconstruction loss $\|x - g(f(x))\|_2^2$ to learn representations without labels, we run into a limitation: reconstruction loss forces the network to reconstruct *every single pixel* (including background noise). 
>
> In **Node 4**, we will discover **Self-Supervised Pretext Tasks**, where we force the network to learn representations by solving clever domain-specific prediction tasks.
>


> [!question] Node 3 Check — Autoencoder Bottleneck Check
> Node 3 Quiz Check: In a standard convolutional autoencoder, what prevents the network from learning a trivial identity mapping g(f(x)) = x that merely copies pixels without learning meaningful semantic representations?
>
> 1. The latent bottleneck dimension m = dim(z) is significantly smaller than input dimension n = dim(x), forcing information compression.
> 2. The encoder uses manual human labels y to constrain latent vector coordinates during forward propagation.
> 3. The decoder applies L2 normalization to force all output pixel values onto a 2D unit circle.
> 4. The loss function uses softmax cross-entropy over classification categories instead of pixel reconstruction error.


> [!success] Quiz — correct ✓
> Your answer: 1. The latent bottleneck dimension m = dim(z) is significantly smaller than input dimension n = dim(x), forcing information compression.
> Correct answer: 1
>
> Correct! Because m << n, the network lacks the capacity to store all raw pixels, forcing it to compress data and extract core underlying semantic features.


> [!abstract] Node 4 — Self-Supervised Pretext Tasks
> ## Node 4: Self-Supervised Pretext Tasks ("Cooking Up Labels")
>
> ### 1. Motivation: Beyond Simple Pixel Reconstruction
> Standard Autoencoders optimize pixel-level reconstruction error $\|x - \hat{x}\|_2^2$. However, this forces the network to spend equal capacity reconstructing irrelevant background pixels (like plain sky or wall texture).
>
> **Self-Supervised Learning (SSL)** solves this by framing unsupervised representation learning as a pseudo-supervised problem. We **"cook up labels"** directly from raw data by hiding/modifying a portion of the input and forcing the network to predict the missing part.
>
> ---
>
> ### 2. Three Classic Self-Supervised Pretext Tasks
>
> ```mermaid
> flowchart TD
>     SSL["Self-Supervised Pretext Tasks"]
>     SSL --> Colorization["1. CIE L*a*b* Colorization<br/>(Predict ab channels from L)"]
>     SSL --> ADAS["2. ADAS Video Depth Estimation<br/>(Temporal 3D Reprojection Error)"]
>     SSL --> MAE["3. Masked Autoencoders (MAE)<br/>(Mask 75%+ Patches vs 15% BERT MLM)"]
> ```
>
> #### **A. Image Colorization ($L*a*b*$ Color Space Split)**
> - Instead of RGB, convert images to **CIE $L*a*b*$ color space**:
>   - $L \in \mathbb{R}^{H \times W \times 1}$: Luminance channel (Grayscale intensity).
>   - $ab \in \mathbb{R}^{H \times W \times 2}$: Chrominance channels (Color spectrum).
> - **Pretext Task**: Input grayscale $L$ to encoder $f(L)$, and predict color channels $\hat{a b} = g(f(L))$.
> - **Why it forces semantic understanding**: To correctly paint a tree green, water blue, or a fish orange, the network *must* recognize object boundaries and semantics—all without human labels!
>
> ```
> [ Grayscale L Channel (H x W x 1) ] ──► ( Encoder f ) ──► [ Latent z ] ──► ( Decoder g ) ──► [ Predicted ab Channels (H x W x 2) ]
> ```
>
> ---
>
> #### **B. Sequential Video Depth Estimation (ADAS Autonomous Driving)**
> - Dashcams capture video at high rates (e.g., 60 FPS). Consecutive frames $I_t$ and $I_{t+1}$ are temporally adjacent.
> - **Pretext Task**:
>   1. Input frame $I_t$ to predict 3D depth map $D_t$.
>   2. Use camera motion and $D_t$ to reproject 3D pixels forward in time to predict frame $\hat{I}_{t+1}$.
>   3. Compute photometric warping loss $\mathcal{L}_{\text{photo}} = \|I_{t+1} - \hat{I}_{t+1}\|_2^2$.
> - The physical world's temporal consistency provides the self-supervision signal!
>
> ---
>
> #### **C. Masked Autoencoders (MAE) vs. BERT Masked Language Modeling (MLM)**
> - **MAE / Masked Image Modeling (He et al., 2021)**: Divide an image into non-overlapping patches. Mask out a **very high ratio (75% to 80%)** of patches. Feed only the remaining 20-25% unmasked patches to a Vision Transformer encoder. The decoder reconstructs missing pixel patches.
> - **BERT MLM (Devlin et al., 2018)**: Mask **15%** of text tokens in a sentence and predict missing words.
>
> ```
> ┌───────────────────────────────┬───────────────────────────────┐
> │     BERT Masked Language      │   Masked Autoencoders (MAE)   │
> ├───────────────────────────────┼───────────────────────────────┤
> │ Text Tokens (Discrete)        │ Image Patches (Continuous)    │
> │ Mask Ratio: ~15%              │ Mask Ratio: 75% - 80%         │
> │ High information density      │ High spatial redundancy       │
> └───────────────────────────────┴───────────────────────────────┘
> ```
>
> **Why is the Image Mask Ratio (75%) so much higher than Text (15%)?**
> - **Text** is information-dense: removing 15% of words creates a hard puzzle because each word carries discrete semantic meaning.
> - **Images** are spatially redundant: neighboring pixels/patches look almost identical. If you only mask 15% of image patches, the model easily interpolates adjacent pixels (a trivial "shortcut" solution). Masking 75%+ forces the network to learn holistic object representations!
>
> ---
>
> ### 3. Connection
> Self-supervised pretext tasks eliminate the need for manual labels. However, task-specific decoders (like colorization or depth reconstruction) still require generating outputs in the raw data space.
>
> In **Node 5**, we remove decoders entirely! We will study **Metric Learning & Contrastive Loss**, optimizing distances directly in latent vector space $\mathbb{R}^d$.
>


> [!question] Node 4 Check — Self-Supervised Masking Intuition
> Node 4 Quiz Check: Why do Masked Autoencoders (MAE) in computer vision require a very high patch masking ratio (~75% to 80%), whereas BERT in NLP requires a much smaller token masking ratio (~15%)?
>
> 1. Images contain high spatial redundancy between adjacent pixels requiring heavy masking to prevent shortcut solutions, whereas text tokens are discrete and highly information-dense.
> 2. Text tokens contain high spatial redundancy requiring low masking, whereas image pixels are discrete and highly information-dense.
> 3. Vision Transformers have less capacity than language models, so they can only process 25% of the input sequence.
> 4. MAE uses cross-entropy loss over discrete categories, while BERT uses continuous L2 reconstruction loss.


> [!success] Quiz — correct ✓
> Your answer: 1. Images contain high spatial redundancy between adjacent pixels requiring heavy masking to prevent shortcut solutions, whereas text tokens are discrete and highly information-dense.
> Correct answer: 1
>
> Correct! Image pixels are heavily correlated spatially. If only 15% of patches were masked, the network could trivially interpolate neighboring pixels without learning semantic object concepts. Heavy 75%+ masking forces holistic visual reasoning.


> [!abstract] Node 5 — Distance Metrics, Triplet Loss & Negative Mining
> ## Node 5: Distance Metrics, Triplet Loss & Negative Mining
>
> ### 1. Motivation: Metric Learning without Decoders
> Why decode back to raw pixel space at all? For tasks like face recognition, visual search (e.g., Google Photos similarity search), or image retrieval, we don't want reconstructed pixels. 
>
> We want to manipulate distances **directly in latent space $\mathbb{R}^d$**:
> - **Similar items** (e.g., two photos of the same person) should be pulled close together ($d \to 0$).
> - **Dissimilar items** (e.g., photos of different people) should be pushed far apart beyond a distance threshold.
>
> ---
>
> ### 2. Establishing Metric Formulations & Triplet Loss
>
> #### **A. Cosine Similarity vs. Euclidean Distance**
> For latent vectors $u, v \in \mathbb{R}^d$:
> $$\text{sim}(u, v) = \frac{u^\top v}{\|u\|_2 \|v\|_2} = \cos(\theta)$$
>
> - If vectors are L2-normalized ($\|u\|_2 = \|v\|_2 = 1$, as established in Node 2), cosine similarity reduces to simple dot product: $\text{sim}(u, v) = u^\top v$.
>
> ---
>
> #### **B. Triplet Loss Architecture & Derivation (FaceNet)**
> Instead of single images, a **Siamese / Triplet Network** processes three images concurrently through shared encoder weights $f(x)$:
> 1. **Anchor ($x_a$)**: Reference image.
> 2. **Positive ($x_p$)**: Image from the *same* class/person as the anchor.
> 3. **Negative ($x_n$)**: Image from a *different* class/person.
>
> ```
>                   ┌───────────────┐
>   Anchor x_a ────►│ Shared CNN f  │──► f(x_a) ──┐
>                   └───────────────┘             │
>                   ┌───────────────┐             ├──► Triplet Loss L_triplet
>   Positive x_p ──►│ Shared CNN f  │──► f(x_p) ──┤
>                   └───────────────┘             │
>                   ┌───────────────┐             │
>   Negative x_n ──►│ Shared CNN f  │──► f(x_n) ──┘
>                   └───────────────┘
> ```
>
> #### **Mathematical Formulation of Triplet Loss**:
> $$\mathcal{L}_{\text{triplet}}(x_a, x_p, x_n) = \max\left(0, \|f(x_a) - f(x_p)\|_2^2 - \|f(x_a) - f(x_n)\|_2^2 + \epsilon\right)$$
>
> Where $\epsilon > 0$ is the enforced **margin distance**.
>
> **Instructor's Step-by-Step Mathematical Walkthrough**:
> - Let $d(x_a, x_p) = \|f(x_a) - f(x_p)\|_2^2$ be the positive pair distance.
> - Let $d(x_a, x_n) = \|f(x_a) - f(x_n)\|_2^2$ be the negative pair distance.
> - We want the negative pair to be further than the positive pair by at least margin $\epsilon$:
>   $$d(x_a, x_p) + \epsilon \le d(x_a, x_n) \implies d(x_a, x_p) - d(x_a, x_n) + \epsilon \le 0$$
> - **Why $\max(0, \dots)$?** Distance metrics cannot be negative. If the margin condition is satisfied, the loss term is negative, so $\max(0, \text{negative}) = 0$ (Zero Loss! Model parameters require no update).
> - If the negative point is too close, the term becomes positive, generating gradient signals that pull $f(x_p)$ closer to $f(x_a)$ and push $f(x_n)$ outside the margin boundary!
>
> ---
>
> #### **C. Negative Sample Mining Taxonomy (Hard vs. Semi-Hard vs. Easy)**
> If you select triplets randomly, most negative images will be easy negatives (e.g., comparing a cat to an airplane), giving $d(x_a, x_n) \gg d(x_a, x_p) + \epsilon$. The loss is $0$, providing zero gradient update to the network!
>
> To train effectively, we perform **Negative Mining**:
>
> ```
>                               Anchor f(x_a)
>                                    │
>             ┌──────────────────────┴──────────────────────┐
>             ▼                                             ▼
>   [ d(x_a, x_p) ]                               [ d(x_a, x_p) + ε ]
>  (Positive Distance)                            (Margin Boundary)
>             │                                             │
>  ◄──────────┴──────────────────────┬──────────────────────┴──────────►
>      HARD NEGATIVE                 │      SEMI-HARD NEGATIVE     │  EASY NEGATIVE
>   d(x_a, x_n) < d(x_a, x_p)        │ d(x_a,p) < d(x_a,n) < +ε    │ d(x_a,n) > d(a,p)+ε
>   (Model misplaces negative        │ (Further than positive,     │ (Zero loss;
>    closer than positive!)          │  but inside margin ε)       │  no update)
> ```
>
> 1. **Hard Negatives**: $d(x_a, x_n) < d(x_a, x_p)$. The model incorrectly places the negative sample *closer* to the anchor than the positive sample! (Maximum gradient update).
> 2. **Semi-Hard Negatives**: $d(x_a, x_p) < d(x_a, x_n) < d(x_a, x_p) + \epsilon$. The negative sample is further than the positive sample, but still violates the safety margin $\epsilon$.
> 3. **Easy Negatives**: $d(x_a, x_n) > d(x_a, x_p) + \epsilon$. Satisfies margin constraint perfectly (Zero loss).
>
> ---
>
> ### 3. Connection & Complete Graph Synthesis
> Notice how this brings our entire lesson full circle:
> 1. We started in **Node 1** with forward encoder mapping $z = f(x)$.
> 2. In **Node 2**, we applied **L2 Normalization** to project vectors onto a unit hypersphere $\mathbb{S}^{d-1}$.
> 3. In **Node 3 & 4**, we explored unsupervised autoencoders and self-supervised pretext tasks.
> 4. In **Node 5**, by applying **Triplet Loss** with **Semi-Hard Negative Mining** on L2-normalized embeddings, we form compact, perfectly separated clusters in latent space! This powers production visual search engines like Google Photos.
>


> [!question] Node 5 Check — Triplet Loss Negative Mining Verification
> Node 5 Quiz Check: In Triplet Loss optimization with margin \epsilon, suppose d(x_a, x_p) = 0.4 while d(x_a, x_n) = 0.3. How is this negative sample categorized?
>
> 1. Hard Negative (since d(x_a, x_n) < d(x_a, x_p), meaning the model misplaces the negative sample closer to the anchor than the positive sample).
> 2. Semi-Hard Negative (since d(x_a, x_p) < d(x_a, x_n) < d(x_a, x_p) + \epsilon).
> 3. Easy Negative (since d(x_a, x_n) > d(x_a, x_p) + \epsilon).
> 4. Zero-Loss Negative (since distance metrics cannot be negative).


> [!success] Quiz — correct ✓
> Your answer: 1. Hard Negative (since d(x_a, x_n) < d(x_a, x_p), meaning the model misplaces the negative sample closer to the anchor than the positive sample).
> Correct answer: 1
>
> Correct! Because d(x_a, x_n) = 0.3 < 0.4 = d(x_a, x_p), the negative sample is closer to the anchor than the positive sample! This is a classic Hard Negative that generates a strong loss gradient update.


> [!success] Lesson Complete — Representation Learning Mastered ✓
> ### Session Completion & Mastery Summary
>
> Congratulations! You have completed all 5 nodes of **Session 5 — Embeddings & Image Similarity**:
>
> - **Node 1**: Forward Encoder Mapping ($f: \mathcal{X} \to \mathbb{R}^d$) vs Reverse Generative Modeling ($g: \mathbb{R}^d \to \mathcal{X}$).
> - **Node 2**: Geometric Layer Transformations (Linear affine shifts, ReLU quadrant folding, L2 norm unit circle $x_1^2 + x_2^2 = 1$ projection, and Softmax $p_1 + p_2 = 1$ probability simplex).
> - **Node 3**: Representation Learning Taxonomy & Autoencoders ($\|x - g(f(x))\|_2^2$ reconstruction loss with $m \ll n$ bottleneck).
> - **Node 4**: Self-Supervised Pretext Tasks ($L*a*b*$ colorization, ADAS 3D video reprojection depth estimation, and 75%+ Masked Autoencoders vs 15% BERT MLM).
> - **Node 5**: Metric Learning, Cosine Similarity, Triplet Loss $\max(0, d(a,p) - d(a,n) + \epsilon)$, and Hard vs Semi-Hard Negative Mining.
>
> Your live lesson log is fully saved in [Representation Learning.md](file:///home/manav/learn/Representation%20Learning.md).
