import API from "./api";

/* ==============================
   ADMIN ANALYTICS (Dashboard)
============================== */
export const fetchAdminAnalytics = async () => {
  const res = await API.get("/admin/analytics");
  return res.data;
};

/* ==============================
   ORGANIZATION USERS
============================== */
export const fetchOrgUsers = async () => {
  const res = await API.get("/users/org-users");
  return res.data;
};

/* ==============================
   DELETE USER
============================== */
export const deleteUser = async (userId: number) => {
  const res = await API.delete(`/users/delete-user/${userId}`);
  return res.data;
};

/* ==============================
   UPDATE USER ROLE
============================== */
export const updateUserRole = async (
  userId: number,
  newRole: string
) => {
  const res = await API.put(
    `/users/update-user-role/${userId}?new_role=${newRole}`
  );
  return res.data;
};