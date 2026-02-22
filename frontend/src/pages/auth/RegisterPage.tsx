import { useState } from "react";
import API from "../../services/api";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";

const RegisterPage = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    organization_name: "",
    email: "",
    password: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      await API.post("/users/register", form);
      toast.success("Registration successful 🎉");
      navigate("/login");
    } catch (error: any) {
      toast.error(
        error?.response?.data?.detail || "Registration failed"
      );
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-black text-white">
      <form
        onSubmit={handleSubmit}
        className="bg-gray-900 p-8 rounded-xl w-96 shadow-xl space-y-4"
      >
        <h1 className="text-2xl font-bold text-center">
          Create Organization Account
        </h1>

        <input
          name="organization_name"
          placeholder="Organization Name"
          className="w-full p-3 bg-gray-800 rounded"
          onChange={handleChange}
        />

        <input
          name="email"
          type="email"
          placeholder="Email"
          className="w-full p-3 bg-gray-800 rounded"
          onChange={handleChange}
        />

        <input
          name="password"
          type="password"
          placeholder="Password"
          className="w-full p-3 bg-gray-800 rounded"
          onChange={handleChange}
        />

        <button
          type="submit"
          className="w-full p-3 bg-purple-600 hover:bg-purple-700 rounded"
        >
          Register
        </button>
      </form>
    </div>
  );
};

export default RegisterPage;