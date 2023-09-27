import styled from 'styled-components';
import './App.css';
import AppRoutes from './AppRoutes';
import Navbar from './containers/Nav/Navbar';

const AppContainer = styled.div`
  display: flex;
  height: 100vh;
`;

function App() {
  return (
    <AppContainer>
    <Navbar />
    <AppRoutes />
    </AppContainer>
  );
}

export default App;
