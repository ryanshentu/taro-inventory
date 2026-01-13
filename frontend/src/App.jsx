import { useState, useEffect } from 'react'
import axios from 'axios'

function App() {
  const [inventory, setInventory] = useState([])
  const [loading, setLoading] = useState(true)

  // 1. Fetch Data from Python Backend
  const fetchInventory = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/inventory')
      setInventory(response.data)
      setLoading(false)
    } catch (error) {
      console.error("Error connecting to backend:", error)
    }
  }

  // Run this when the page loads
  useEffect(() => {
    fetchInventory()
  }, [])

  // 2. Function to Handle a Sale
  const handleSale = async (itemName) => {
    try {
      await axios.post('http://127.0.0.1:8000/sale', {
        name: itemName,
        amount_used: 1 
      })
      fetchInventory() // Refresh the list immediately
    } catch (error) {
      alert("Error processing sale")
    }
  }

  return (
    // FORCE BLACK TEXT AND WHITE BACKGROUND HERE
    <div style={{ padding: "40px", fontFamily: "Arial, sans-serif", color: "black", backgroundColor: "white", minHeight: "100vh" }}>
      <h1>🥤 Taro Inventory Manager</h1>
      
      {loading ? <p>Loading data...</p> : (
        <table border="1" cellPadding="10" style={{ borderCollapse: "collapse", width: "100%", borderColor: "#ddd" }}>
          <thead>
            <tr style={{ background: "#f0f0f0", color: "black" }}>
              <th style={{ textAlign: "left" }}>Item Name</th>
              <th style={{ textAlign: "left" }}>Quantity</th>
              <th style={{ textAlign: "left" }}>Status</th>
              <th style={{ textAlign: "left" }}>Action</th>
            </tr>
          </thead>
          <tbody>
            {inventory.map((item) => (
              <tr key={item.id} style={{ background: item.quantity < item.threshold ? "#ffcccc" : "white" }}>
                <td>{item.name}</td>
                <td>{item.quantity} {item.unit}</td>
                <td>
                  {item.quantity < item.threshold ? (
                    <span style={{ color: "red", fontWeight: "bold" }}>⚠️ LOW STOCK</span>
                  ) : (
                    <span style={{ color: "green", fontWeight: "bold" }}>OK</span>
                  )}
                </td>
                <td>
                  <button 
                    onClick={() => handleSale(item.name)} 
                    style={{ 
                      cursor: "pointer", 
                      padding: "5px 10px", 
                      backgroundColor: "#007bff", 
                      color: "white", 
                      border: "none", 
                      borderRadius: "4px" 
                    }}
                  >
                    Sell 1 Unit
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default App