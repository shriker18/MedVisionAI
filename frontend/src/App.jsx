import { useState } from "react";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState(
    "Describe the important visible findings in this medical image. Be conservative and mention uncertainty."
  );
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function analyzeImage() {
    if (!file) {
      setError("Please select a medical image first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("question", question);

    try {
      const response = await fetch(
        `${API_URL}/analysis/image`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Analysis failed.");
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleFileChange(event) {
    const selected = event.target.files?.[0];

    setFile(selected || null);
    setResult(null);
    setError("");
  }

  return (
    <div className="app">
      <nav className="navbar">
        <div className="brand">
          <div className="brand-mark">M</div>

          <div>
            <div className="brand-name">MedVision</div>
            <div className="brand-subtitle">Medical AI Platform</div>
          </div>
        </div>

        <div className="nav-links">
          <a className="active">Dashboard</a>
          <a>History</a>
          <a>About</a>
        </div>

        <div className="api-status">
          <span className="status-dot"></span>
          API Online
        </div>
      </nav>

      <main>
        <section className="hero">
          <div className="hero-badge">
            <span>✦</span>
            MULTIMODAL AI
          </div>

          <h1>
            Medical imaging,
            <br />
            <span>interpreted intelligently.</span>
          </h1>

          <p>
            Upload a medical image and use MedGemma to generate
            conservative, AI-assisted visual findings for clinical review.
          </p>
        </section>

        <section className="workspace">
          <div className="panel upload-panel">
            <div className="panel-header">
              <div>
                <div className="section-label">STEP 01</div>
                <h2>Upload image</h2>
              </div>

              <div className="step-number">01</div>
            </div>

            <label className="upload-area">
              <input
                type="file"
                accept="image/jpeg,image/png,image/webp"
                onChange={handleFileChange}
              />

              {!file ? (
                <>
                  <div className="upload-symbol">+</div>

                  <strong>Select a medical image</strong>

                  <span>
                    Drag and drop or click to browse
                  </span>

                  <small>
                    JPEG, PNG or WEBP · Maximum 10 MB
                  </small>
                </>
              ) : (
                <>
                  <div className="file-symbol">✓</div>

                  <strong>{file.name}</strong>

                  <span>Image selected successfully</span>

                  <small>Click to choose another image</small>
                </>
              )}
            </label>

            {file && (
              <div className="image-preview">
                <img
                  src={URL.createObjectURL(file)}
                  alt="Selected medical image"
                />
              </div>
            )}

            <div className="field">
              <label>Clinical question</label>

              <textarea
                value={question}
                onChange={(event) =>
                  setQuestion(event.target.value)
                }
                rows={5}
                placeholder="Ask the model what you want it to examine..."
              />
            </div>

            <button
              className="primary-button"
              onClick={analyzeImage}
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="button-spinner"></span>
                  Analyzing image...
                </>
              ) : (
                <>
                  Analyze image
                  <span>→</span>
                </>
              )}
            </button>

            {error && (
              <div className="error-message">
                <span>!</span>
                {error}
              </div>
            )}
          </div>

          <div className="panel analysis-panel">
            <div className="panel-header">
              <div>
                <div className="section-label">STEP 02</div>
                <h2>AI analysis</h2>
              </div>

              {result && (
                <div className="complete-badge">
                  <span>✓</span>
                  COMPLETE
                </div>
              )}
            </div>

            {!result && !loading && (
              <div className="analysis-empty">
                <div className="empty-visual">
                  <div className="scan-line"></div>
                  <span>✦</span>
                </div>

                <h3>Ready for analysis</h3>

                <p>
                  Your AI-generated findings will appear here
                  after you upload an image and start an analysis.
                </p>

                <div className="model-chip">
                  <span>●</span>
                  MedGemma 1.5 · 4B
                </div>
              </div>
            )}

            {loading && (
              <div className="analysis-empty">
                <div className="loading-visual">
                  <div></div>
                </div>

                <h3>Analyzing image</h3>

                <p>
                  MedGemma is processing the image.
                  The first request may take several minutes
                  while the model loads.
                </p>

                <div className="processing-bar">
                  <div></div>
                </div>
              </div>
            )}

            {result && (
              <div className="result">
                <div className="result-meta">
                  <div>
                    <span>MODEL</span>
                    <strong>MedGemma 1.5 · 4B</strong>
                  </div>

                  <div>
                    <span>IMAGE</span>
                    <strong>
                      {result.metadata.width} ×{" "}
                      {result.metadata.height}
                    </strong>
                  </div>

                  <div>
                    <span>FORMAT</span>
                    <strong>{result.metadata.format}</strong>
                  </div>
                </div>

                <div className="finding-section">
                  <div className="finding-heading">
                    <span className="finding-icon">✦</span>

                    <div>
                      <div className="section-label">
                        AI-GENERATED
                      </div>
                      <h3>Visual findings</h3>
                    </div>
                  </div>

                  <div className="finding-text">
                    {result.analysis}
                  </div>
                </div>

                <div className="warning-box">
                  <div className="warning-icon">!</div>

                  <div>
                    <strong>Clinical review required</strong>

                    <p>
                      This output is AI-generated and should not
                      be interpreted as a medical diagnosis.
                      Qualified clinical review is required.
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </section>

        <section className="pipeline">
          <div className="pipeline-title">
            <span>HOW IT WORKS</span>
            <strong>From image to insight</strong>
          </div>

          <div className="pipeline-flow">
            <div className="pipeline-step">
              <div className="pipeline-icon">01</div>
              <div>
                <strong>Upload</strong>
                <span>Medical image</span>
              </div>
            </div>

            <div className="pipeline-line"></div>

            <div className="pipeline-step">
              <div className="pipeline-icon">02</div>
              <div>
                <strong>Validate</strong>
                <span>Format & size checks</span>
              </div>
            </div>

            <div className="pipeline-line"></div>

            <div className="pipeline-step">
              <div className="pipeline-icon">03</div>
              <div>
                <strong>Analyze</strong>
                <span>MedGemma inference</span>
              </div>
            </div>

            <div className="pipeline-line"></div>

            <div className="pipeline-step">
              <div className="pipeline-icon">04</div>
              <div>
                <strong>Explain</strong>
                <span>AI-assisted findings</span>
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer>
        <div>
          <strong>MedVision</strong>
          <span>Research & Educational Prototype</span>
        </div>

        <span>
          AI output is not a medical diagnosis.
        </span>
      </footer>
    </div>
  );
}

export default App;