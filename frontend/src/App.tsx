import { useRef, useState } from "react";
import {
  Activity,
  Binary,
  Check,
  FileCode2,
  Hash,
  Upload,
  Zap,
} from "lucide-react";

import "./App.css";

type MathCodecResult = {
  format: string;
  version: string;
  id: string;
  data_type: string;
  original_size: number;
  method: string;
  modulus: number;
  multiplier: number;
  offset: number;
  encoded_data: number[];
  sha256: string;
  equation: string;
  filename?: string;
};

function App() {
  const fileInput = useRef<HTMLInputElement>(null);

  const [result, setResult] = useState<MathCodecResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function encodeFile(file: File) {
    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();

    formData.append("file", file);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/encode",
        {
          method: "POST",
          body: formData,
        },
      );

      if (!response.ok) {
        throw new Error("Encoding failed.");
      }

      const data: MathCodecResult =
        await response.json();

      setResult(data);
    } catch {
      setError(
        "CONNECTION FAILURE :: Is MathCodec API running?"
      );
    } finally {
      setLoading(false);
    }
  }

  function selectFile(file?: File) {
    if (!file) {
      return;
    }

    encodeFile(file);
  }

  function formatBytes(bytes: number) {
    if (bytes < 1024) {
      return `${bytes} B`;
    }

    if (bytes < 1024 * 1024) {
      return `${(bytes / 1024).toFixed(2)} KB`;
    }

    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  }

  return (
    <div className="terminal-shell">

      <header className="terminal-header">
        <div className="brand">
          <div className="brand-icon">
            <Binary size={18} />
          </div>

          <div>
            <div className="brand-title">
              MATHCODEC
            </div>

            <div className="brand-subtitle">
              REVERSIBLE DATA SYSTEM
            </div>
          </div>
        </div>

        <div className="header-status">
          <span className="status-light" />
          SYSTEM ONLINE
        </div>
      </header>


      <main>

        <section className="boot-message">

          <div>
            &gt; MATHCODEC TERMINAL
          </div>

          <div>
            &gt; REVERSIBLE MATHEMATICAL DATA REPRESENTATION
          </div>

          <div>
            &gt; VERSION 0.1.0
          </div>

          <div>
            &gt; LOCAL PROCESSING ENABLED
          </div>

        </section>


        <section
          className="upload-terminal"
          onClick={() =>
            fileInput.current?.click()
          }
        >

          <input
            ref={fileInput}
            type="file"
            hidden
            onChange={(event) =>
              selectFile(
                event.target.files?.[0]
              )
            }
          />

          <Upload size={25} />

          <div className="upload-title">
            {loading
              ? "PROCESSING..."
              : "INSERT DATA"}
          </div>

          <div className="upload-description">
            SELECT FILE TO BEGIN ENCODING
          </div>

          <div className="upload-command">
            [ CLICK TO SELECT ]
          </div>

        </section>


        {error && (
          <section className="error-box">
            <div>
              [ ERROR ]
            </div>

            <p>{error}</p>
          </section>
        )}


        {result && (
          <section className="result-terminal">

            <div className="terminal-section-title">
              <Activity size={15} />
              REPRESENTATION GENERATED
            </div>


            <div className="equation-panel">

              <div className="label">
                MATHEMATICAL TRANSFORMATION
              </div>

              <div className="equation">
                {result.equation}
              </div>

              <div className="equation-note">
                BYTE TRANSFORMATION / MODULAR ARITHMETIC
              </div>

            </div>


            <div className="data-grid">

              <div className="data-cell">
                <span>FILE</span>
                <strong>
                  {result.filename}
                </strong>
              </div>

              <div className="data-cell">
                <span>SIZE</span>
                <strong>
                  {formatBytes(
                    result.original_size
                  )}
                </strong>
              </div>

              <div className="data-cell">
                <span>METHOD</span>
                <strong>
                  {result.method}
                </strong>
              </div>

              <div className="data-cell">
                <span>MODULUS</span>
                <strong>
                  {result.modulus}
                </strong>
              </div>

            </div>


            <div className="parameter-terminal">

              <div className="label">
                MODEL PARAMETERS
              </div>

              <div className="parameter">
                <span>MULTIPLIER</span>
                <code>
                  {result.multiplier}
                </code>
              </div>

              <div className="parameter">
                <span>OFFSET</span>
                <code>
                  {result.offset}
                </code>
              </div>

              <div className="parameter">
                <span>MODULUS</span>
                <code>
                  {result.modulus}
                </code>
              </div>

              <div className="parameter">
                <span>ENCODED VALUES</span>
                <code>
                  {result.encoded_data.length}
                </code>
              </div>

            </div>


            <div className="identity-panel">

              <div className="identity-icon">
                <Hash size={18} />
              </div>

              <div>

                <div className="label">
                  REPRESENTATION ID
                </div>

                <div className="identity-value">
                  {result.id}
                </div>

              </div>

            </div>


            <div className="hash-panel">

              <div>

                <div className="label">
                  SHA-256 INTEGRITY
                </div>

                <code>
                  {result.sha256}
                </code>

              </div>

              <Check size={20} />

            </div>


            <div className="proof-panel">

              <div className="proof-equation">
                D(E(X)) = X
              </div>

              <div>

                <strong>
                  LOSSLESS RECONSTRUCTION
                </strong>

                <p>
                  ORIGINAL BYTE SEQUENCE
                  CAN BE RECOVERED EXACTLY.
                </p>

              </div>

            </div>

          </section>
        )}

      </main>


      <footer>

        <span>
          MATHCODEC // LOCAL TERMINAL
        </span>

        <span>
          PYTHON + FASTAPI + REACT
        </span>

      </footer>

    </div>
  );
}

export default App;