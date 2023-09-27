import React from "react";
import { Route, Routes } from "react-router-dom";
import styled from "styled-components";
import Home from "./containers/Home";
import Chat from "./containers/Chat";

const AppRoutes: React.FC<{}> = () => {
    return (
      <AppContainer>
        <Routes>
        <Route
            path="/"
            element={
            <Home />
            }
        />
        <Route
            path="/chat"
            element={
            <Chat />
            }
        />
        <Route path="*" element={<h1>Not Found</h1>} />
        </Routes>
      </AppContainer>
    );
  };

const AppContainer = styled.div`
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100vh;
`;

export default AppRoutes;