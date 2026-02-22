import { useEffect, useState } from "react";
import {
  fetchOrgUsers,
  deleteUser,
  updateUserRole,
} from "../../services/adminService";
import AdminUsersTable from "../../components/admin/AdminUsersTable";

export default function AdminUsersPage() {
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const loadUsers = async () => {
    try {
      const data = await fetchOrgUsers();
      setUsers(data);
    } catch (error) {
      console.error("Failed to fetch users");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUsers();
  }, []);

  const handleDelete = async (id: number) => {
    await deleteUser(id);
    loadUsers();
  };

  const handleRoleChange = async (id: number, role: string) => {
    await updateUserRole(id, role);
    loadUsers();
  };

  if (loading) {
    return <div className="p-8 text-white">Loading users...</div>;
  }

  return (
    <div className="p-8">
      <h1 className="text-2xl text-white mb-6">Organization Users</h1>
      <AdminUsersTable
        users={users}
        onDelete={handleDelete}
        onRoleChange={handleRoleChange}
      />
    </div>
  );
}