import { useState } from 'react'
import './ResultDisplay.css'

const ResultDisplay = ({ result, onReset }) => {
  const [copied, setCopied] = useState(false)

  const handleCopy = () => {
    const jsonString = JSON.stringify(result.extracted_data, null, 2)
    navigator.clipboard.writeText(jsonString)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const renderJSON = (data, level = 0) => {
    if (data === null) return <span className="json-null">null</span>
    if (typeof data === 'boolean') return <span className="json-boolean">{data.toString()}</span>
    if (typeof data === 'number') return <span className="json-number">{data}</span>
    if (typeof data === 'string') return <span className="json-string">"{data}"</span>

    if (Array.isArray(data)) {
      if (data.length === 0) return <span className="json-bracket">[]</span>
      return (
        <div className="json-array">
          <span className="json-bracket">[</span>
          <div className="json-content" style={{ marginLeft: `${(level + 1) * 20}px` }}>
            {data.map((item, index) => (
              <div key={index} className="json-item">
                {renderJSON(item, level + 1)}
                {index < data.length - 1 && <span className="json-comma">,</span>}
              </div>
            ))}
          </div>
          <span className="json-bracket">]</span>
        </div>
      )
    }

    if (typeof data === 'object') {
      const keys = Object.keys(data)
      if (keys.length === 0) return <span className="json-bracket">{'{}'}</span>
      return (
        <div className="json-object">
          <span className="json-bracket">{'{'}</span>
          <div className="json-content" style={{ marginLeft: `${(level + 1) * 20}px` }}>
            {keys.map((key, index) => (
              <div key={key} className="json-item">
                <span className="json-key">"{key}"</span>
                <span className="json-colon">: </span>
                {renderJSON(data[key], level + 1)}
                {index < keys.length - 1 && <span className="json-comma">,</span>}
              </div>
            ))}
          </div>
          <span className="json-bracket">{'}'}</span>
        </div>
      )
    }

    return <span>{String(data)}</span>
  }

  return (
    <div className="result-container">
      <div className="result-header">
        <h2>✅ Extraction Complete</h2>
        <p className="filename">File: {result.filename}</p>
      </div>

      <div className="json-display">
        <div className="json-header">
          <h3>Extracted Data</h3>
          <div className="json-actions">
            <button onClick={handleCopy} className="btn-copy">
              {copied ? '✓ Copied!' : '📋 Copy JSON'}
            </button>
          </div>
        </div>
        <div className="json-viewer">
          {renderJSON(result.extracted_data)}
        </div>
      </div>

      <div className="result-actions">
        <button onClick={onReset} className="btn-primary">
          Upload Another Image
        </button>
      </div>

      <div className="info-box">
        <p>💡 <strong>Note:</strong> This AI extracts only what it can read from the handwriting. If some text is unclear or illegible, it may be marked as "unreadable" or omitted.</p>
      </div>
    </div>
  )
}

export default ResultDisplay
