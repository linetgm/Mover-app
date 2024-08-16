import React, { createContext, useState } from 'react';

export const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState({ id: null, username: '', email: '', role: '' });
  const [company, setCompany] = useState({ id: null, name: '', email: '', role: '' });

  return (
    <UserContext.Provider value={{ user, setUser, company, setCompany }}>
      {children}
    </UserContext.Provider>
  );
};
// import React, { createContext, useState, useContext } from 'react';

// const UserContext = createContext();

// export const UserProvider = ({ children }) => {
//   const [isAuthenticated, setIsAuthenticated] = useState(false);
  
//   const login = () => {
//     setIsAuthenticated(true);
//   };

//   const logout = () => {
//     setIsAuthenticated(false);
//   };

//   return (
//     <UserContext.Provider value={{ isAuthenticated, login, logout }}>
//       {children}
//     </UserContext.Provider>
//   );
// };

// export const useUser = () => useContext(UserContext);
