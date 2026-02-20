import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../../services/api";

declare global {
  interface Window {
    Razorpay: any;
  }
}

export default function UpgradePage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [scriptLoaded, setScriptLoaded] = useState(false);

  // ==============================
  // Load Razorpay Script Properly
  // ==============================
  useEffect(() => {
    const script = document.createElement("script");
    script.src = "https://checkout.razorpay.com/v1/checkout.js";
    script.async = true;

    script.onload = () => {
      console.log("✅ Razorpay script loaded");
      setScriptLoaded(true);
    };

    script.onerror = () => {
      console.error("❌ Razorpay script failed to load");
    };

    document.body.appendChild(script);
  }, []);

  // ==============================
  // Handle Payment
  // ==============================
  const handlePayment = async () => {
    if (!scriptLoaded) {
      alert("Payment system not ready. Please refresh.");
      return;
    }

    try {
      setLoading(true);

      // 1️⃣ Create order from backend
      const orderRes = await API.post("/payments/create-order");

      const { order_id, amount, key } = orderRes.data;

      console.log("🧾 Order created:", orderRes.data);

      const options = {
        key: key,
        amount: amount,
        currency: "INR",
        name: "Life Signify NumAI",
        description: "Pro Plan Upgrade",
        order_id: order_id,

        // ==============================
        // SUCCESS HANDLER
        // ==============================
        handler: async function (response: any) {
          console.log("🔥 Razorpay SUCCESS response:", response);

          try {
            const verifyRes = await API.post("/payments/verify", {
              razorpay_order_id: response.razorpay_order_id,
              razorpay_payment_id: response.razorpay_payment_id,
              razorpay_signature: response.razorpay_signature,
            });

            console.log("✅ Payment verified:", verifyRes.data);

            alert("Payment Successful! 🎉");

            navigate("/dashboard");
          } catch (error: any) {
            console.error("❌ Verification failed:", error.response?.data || error);
            alert("Payment verification failed.");
          }
        },

        // ==============================
        // FAILURE HANDLER
        // ==============================
        modal: {
          ondismiss: function () {
            console.log("❌ Razorpay popup closed by user");
            setLoading(false);
          },
        },

        // ==============================
        // Payment Failed Event
        // ==============================
        handler_error: function (error: any) {
          console.error("❌ Razorpay error:", error);
          setLoading(false);
        },

        theme: {
          color: "#6366f1",
        },
      };

      const rzp = new window.Razorpay(options);

      rzp.on("payment.failed", function (response: any) {
        console.error("❌ Payment failed event:", response);
        alert("Payment failed. Please try again.");
        setLoading(false);
      });

      rzp.open();
    } catch (error: any) {
      console.error("❌ Order creation failed:", error.response?.data || error);
      alert("Unable to initiate payment.");
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black flex items-center justify-center text-white">
      <div className="bg-white/5 p-10 rounded-2xl border border-white/10 text-center space-y-6">
        <h1 className="text-3xl font-bold text-purple-400">
          Upgrade to Pro
        </h1>

        <p className="text-gray-400">
          Unlock unlimited AI reports, premium PDF exports,
          strategic intelligence layers and advanced analytics.
        </p>

        <button
          onClick={handlePayment}
          disabled={loading}
          className="bg-gradient-to-r from-indigo-600 to-purple-600 px-8 py-3 rounded-xl disabled:opacity-50"
        >
          {loading ? "Processing..." : "Upgrade Now – ₹499"}
        </button>
      </div>
    </div>
  );
}