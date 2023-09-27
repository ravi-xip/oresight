import React from "react";
import { NavigateFunction, useLocation, useNavigate } from "react-router-dom";
import styled from "styled-components";
import { AiOutlinePoweroff } from "react-icons/ai";
import { FaFolderOpen, FaRegFolderOpen } from "react-icons/fa";
import { GiHamburgerMenu } from "react-icons/gi";
import { IoHomeOutline, IoHomeSharp } from "react-icons/io5";
import { MdOutlineManageSearch } from "react-icons/md";
import { HamburgerMenuContainer } from "./Navbar";
import {
  borderColor,
  navBackground,
  navBackgroundHover,
  navbarTextSelectedColor,
} from "../../shared/colors";
import { RightCircleOutlined } from "@ant-design/icons";

type NavRowContainerProps = {
  isSelected?: boolean;
};

interface NavbarCollapsedProps {
  setShowLeftPanel: React.Dispatch<React.SetStateAction<boolean>>;
}

const NavbarCollapsed: React.FC<NavbarCollapsedProps> = ({
  setShowLeftPanel,
}): JSX.Element => {
  return (
    <NavbarOuterContainer>
      <NavbarHamburgerContainer>
        <HamburgerMenuContainer onClick={() => {
          setShowLeftPanel(true);
        }}>
          <RightCircleOutlined style={{ fontSize: '24px' }} />
        </HamburgerMenuContainer>
      </NavbarHamburgerContainer>      
    </NavbarOuterContainer>
  );
};

const NavbarOuterContainer = styled.div`
  display: flex;
  flex-direction: column;
  background-color: transparent;
  color: black;
  z-index: 100;
  height: 100vh;
  width: 50px;
`;

const NavbarHamburgerContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
  height: 50px;
  width: 50px;
  margin-left: 10px;

  &:hover {
    cursor: pointer;
  }
`;



export default NavbarCollapsed;
