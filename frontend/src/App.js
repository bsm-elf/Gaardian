import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";
import GaardianLogo from "./Gaardian.png";

const API_URL = "http://localhost:8000/api"; // Corrected API URL variable

function App() {
  const [settings, setSettings] = useState({
    dry_run: false,
    enable_removal: false,
    auto_import_manual: false,
    auto_handle_custom_format: false,
    auto_remove_unparsable: false,
    auto_remove_qbt_error: false,
    log_level: "info",
    arr_instances: [],
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const response = await axios.get(`${API_URL}/settings`); // Fixed variable name
      setSettings(response.data);
      setLoading(false);
    } catch (err) {
      setError("Failed to fetch settings");
      setLoading(false);
    }
  };

  const updateSettings = async (updatedSettings) => {
    try {
      await axios.post(`${API_URL}/settings`, updatedSettings); // Fixed variable name
      setSettings(updatedSettings);
    } catch (err) {
      setError("Failed to update settings");
    }
  };

  const handleToggle = (key) => {
    const updatedSettings = { ...settings, [key]: !settings[key] };
    setSettings(updatedSettings);
    updateSettings(updatedSettings);
  };

  const handleLogLevelChange = (event) => {
    const updatedSettings = { ...settings, log_level: event.target.value };
    setSettings(updatedSettings);
    updateSettings(updatedSettings);
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="app">
      <div className="logo-container">
        <img src={GaardianLogo} alt="Gaardian Logo" className="logo" />
      </div>
      <h1>Gaardian Settings</h1>
      <div className="settings-container">
        <label>
          <input
            type="checkbox"
            checked={settings.dry_run}
            onChange={() => handleToggle("dry_run")}
          />
          Dry Run
        </label>
        <label>
          Log Level:
          <select value={settings.log_level} onChange={handleLogLevelChange}>
            <option value="info">Info</option>
            <option value="debug">Debug</option>
            <option value="warning">Warning</option>
            <option value="error">Error</option>
          </select>
        </label>
        <label>
          <input
            type="checkbox"
            checked={settings.enable_removal}
            onChange={() => handleToggle("enable_removal")}
          />
          Enable Removal
        </label>
        <label>
          <input
            type="checkbox"
            checked={settings.auto_import_manual}
            onChange={() => handleToggle("auto_import_manual")}
          />
          Auto Import Manual
        </label>
        <label>
          <input
            type="checkbox"
            checked={settings.auto_handle_custom_format}
            onChange={() => handleToggle("auto_handle_custom_format")}
          />
          Auto Handle Custom Format
        </label>
        <label>
          <input
            type="checkbox"
            checked={settings.auto_remove_unparsable}
            onChange={() => handleToggle("auto_remove_unparsable")}
          />
          Auto Remove Unparsable
        </label>
        <label>
          <input
            type="checkbox"
            checked={settings.auto_remove_qbt_error}
            onChange={() => handleToggle("auto_remove_qbt_error")}
          />
          Auto Remove qBittorrent Error
        </label>
      </div>
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default App;
