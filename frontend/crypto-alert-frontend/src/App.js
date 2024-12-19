import React, { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [cryptoPrices, setCryptoPrices] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [userEmail, setUserEmail] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const [formMode, setFormMode] = useState("create");
  const [alertData, setAlertData] = useState({
    crypto_symbol: "DOGEUSDT",
    price_threshold: "",
    condition: "greater",
  });

  const BASE_URL = "https://www.sahitvasu.info/alerts/";

  useEffect(() => {
    const savedEmail = localStorage.getItem("user_email");
    setUserEmail(savedEmail || "");
    if (savedEmail) fetchAlerts(savedEmail); // Fetch alerts on initial load if email is saved
  }, []);

  const updateEmail = () => {
    const email = prompt("Enter your email:");
    if (email) {
      localStorage.setItem("user_email", email);
      setUserEmail(email);
      fetchAlerts(email);
    }
  };

  const fetchAlerts = async (email) => {
    try {
      const response = await fetch(`${BASE_URL}user/${email}`);
      if (response.ok) {
        const data = await response.json();
        setAlerts(data || []);
      } else {
        console.error("Error fetching alerts:", response.statusText);
        setAlerts([]);
      }
    } catch (error) {
      console.error("Error fetching alerts:", error);
    }
  };

  const handleFormSubmit = async () => {
    try {
      const method = formMode === "create" ? "POST" : "PUT";
      const url =
        formMode === "create" ? BASE_URL : `${BASE_URL}${alertData.id}`;
      const response = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...alertData, user_email: userEmail }),
      });
      if (response.ok) {
        fetchAlerts(userEmail);
        setModalOpen(false);
        setAlertData({
          crypto_symbol: "DOGEUSDT",
          price_threshold: "",
          condition: "greater",
        });
      } else {
        console.error("Error saving alert:", response.statusText);
      }
    } catch (error) {
      console.error("Error saving alert:", error);
    }
  };

  const handleDeleteAlert = async (id) => {
    try {
      const response = await fetch(`${BASE_URL}${id}`, { method: "DELETE" });
      if (response.ok) {
        fetchAlerts(userEmail);
      } else {
        console.error("Error deleting alert:", response.statusText);
      }
    } catch (error) {
      console.error("Error deleting alert:", error);
    }
  };

  useEffect(() => {
    const socket = new WebSocket("wss://sahitvasu.info/ws/prices");
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setCryptoPrices(data.crypto_prices || []);
    };
    return () => socket.close();
  }, []);

  return (
    <div className="app">
      <header>
        <h1>Crypto Dashboard</h1>
        <div className="header-right">
          {userEmail && <span className="current-email">{userEmail}</span>}
          <button onClick={updateEmail}>
            {userEmail ? "Change Email" : "Set Email"}
          </button>
        </div>
      </header>

      <section>
        <h2>Live Cryptocurrency Prices</h2>
        <div className="prices-container">
          {Object.entries(cryptoPrices).map(([symbol, price]) => (
            <div className="price-card" key={symbol}>
              <h3>{symbol}</h3>
              <p>${price.toFixed(2)}</p>
            </div>
          ))}
        </div>
      </section>

      <section>
        {!userEmail ? (
          // Case when email is not set
          <div className="email-prompt-container">
            <p>
              Please <button onClick={updateEmail}>set your email</button> to
              view and manage alerts.
            </p>
          </div>
        ) : (
          // Case when email is set, show alerts and create button
          <>
            <h2>Your Alerts</h2>
            <div className="alerts-and-button-container">
              <button
                onClick={() => {
                  setFormMode("create"); // Set to "create" mode
                  setAlertData({
                    crypto_symbol: "DOGEUSDT", // Default symbol
                    price_threshold: "",
                    condition: "above", // Default condition
                  });
                  setModalOpen(true); // Open the modal to create a new alert
                }}
              >
                Create Alert
              </button>

              <div className="alerts-container">
                {alerts.length === 0 ? (
                  <p>No alerts set. Create an alert to get started!</p>
                ) : (
                  alerts.map((alert) => (
                    <div className="alert-card" key={alert.alert_id}>
                      <p>
                        {alert.crypto_symbol} {alert.condition} $
                        {alert.price_threshold}
                      </p>
                      <button
                        onClick={() => {
                          setFormMode("update"); // Set to "update" mode
                          setAlertData(alert); // Pre-fill the form with existing alert data
                          setModalOpen(true); // Open the modal to edit
                        }}
                      >
                        Edit
                      </button>
                      <button onClick={() => handleDeleteAlert(alert.id)}>
                        Delete
                      </button>
                    </div>
                  ))
                )}
              </div>
            </div>
          </>
        )}
      </section>

      {modalOpen && (
        <div className="modal">
          <div className="modal-content">
            <h3>{formMode === "create" ? "Create Alert" : "Update Alert"}</h3>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleFormSubmit();
              }}
            >
              <select
                value={alertData.crypto_symbol}
                onChange={(e) =>
                  setAlertData({ ...alertData, crypto_symbol: e.target.value })
                }
                required
              >
                <option value="DOGEUSDT">DOGEUSDT</option>
                <option value="BTCUSDT">BTCUSDT</option>
                <option value="ETHUSDT">ETHUSDT</option>
                <option value="BNBUSDT">BNBUSDT</option>
                <option value="XRPUSDT">XRPUSDT</option>
              </select>
              <input
                type="number"
                placeholder="Price Threshold"
                value={alertData.price_threshold}
                onChange={(e) =>
                  setAlertData({
                    ...alertData,
                    price_threshold: e.target.value,
                  })
                }
                required
              />
              <select
                value={alertData.condition}
                onChange={(e) =>
                  setAlertData({ ...alertData, condition: e.target.value })
                }
              >
                <option value="above">Above</option>
                <option value="below">Below</option>
              </select>
              <div className="modal-actions">
                <button type="submit">
                  {formMode === "create" ? "Create" : "Update"}
                </button>
                <button type="button" onClick={() => setModalOpen(false)}>
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
