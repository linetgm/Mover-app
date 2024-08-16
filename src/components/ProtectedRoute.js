// components/ProtectedRoute.js
import React from 'react';
import { Route, Navigate } from 'react-router-dom';
import { useContext } from 'react';
import { UserContext } from '../context/UserContext';

const ProtectedRoute = ({ component: Component, roles, ...rest }) => {
  const { user } = useContext(UserContext);

  if (!user.id || (roles && !roles.includes(user.role))) {
    return <Navigate to="/login" />;
  }

  return <Route {...rest} element={<Component />} />;
};

export default ProtectedRoute;
// import React from 'react';
// import { Navigate } from 'react-router-dom';
// import { useUser } from '../context/UserContext'; // Adjust the path as needed

// const ProtectedRoute = ({ element: Element, roles, ...rest }) => {
//   const { isAuthenticated, user } = useUser();

//   // Check if user is authenticated and has required role
//   const hasAccess = isAuthenticated && roles.includes(user?.role);

//   return hasAccess ? <Element {...rest} /> : <Navigate to="/login" />;
// };

// export default ProtectedRoute;
