import React from "react";
import { NavigateFunction, useLocation, useNavigate } from "react-router-dom";
import styled from "styled-components";
import { AiOutlinePoweroff } from "react-icons/ai";
import { IoHomeOutline, IoHomeSharp } from "react-icons/io5";
import { MdOutlineManageSearch } from "react-icons/md";
import { HamburgerMenuContainer } from "./Navbar";
import { IsVisible } from "../../shared/utils";
import { navBackground, borderColor, navbarTextSelectedColor, navBackgroundHover } from "../../shared/colors";
import WebsiteModal from "../../component/WebsiteModal";
import { LeftCircleOutlined } from "@ant-design/icons";

type NavRowContainerProps = {
  isSelected?: boolean;
};

interface NavbarExpandedProps {
  setShowLeftPanel: React.Dispatch<React.SetStateAction<boolean>>;
}

const NavbarExpanded: React.FC<NavbarExpandedProps> = ({
  setShowLeftPanel,
}): JSX.Element => {
  const navigate: NavigateFunction = useNavigate();
  const isAuthenticated: boolean = true;
  const { pathname } = useLocation();

  return (
    <NavBarOuterContainer>
      <AddProspectContainer>
        <WebsiteModal />
        <HamburgerMenuContainer onClick={() => {
          setShowLeftPanel(false);
        }}>
          <LeftCircleOutlined style={{ fontSize: '24px' }} />
        </HamburgerMenuContainer>
      </AddProspectContainer>
      <UpperContainer>
        <NavRowContainer
          onClick={() => {
            navigate("/");
          }}
          isSelected={pathname === "/"}
        >
          <IconContainer>
            {pathname === "/" ? (
              <IoHomeSharp size={24} />
            ) : (
              <IoHomeOutline size={24} />
            )}
          </IconContainer>
          <NavRowText>Home</NavRowText>
        </NavRowContainer>
        <IsVisible condition={isAuthenticated}>
          <NavRowContainer
            onClick={() => {
              navigate("/chat");
            }}
            isSelected={pathname === "/chat"}
          >
            <IconContainer>
              <MdOutlineManageSearch size={30} />
            </IconContainer>
            <NavRowText>Chat</NavRowText>
          </NavRowContainer>
        </IsVisible>
      </UpperContainer>
      <LowerContainer>
        <IsVisible condition={isAuthenticated}>
          <NavRowContainer
            onClick={() => {
              navigate("/logout");
            }}
          >
            <IconContainer>
              <AiOutlinePoweroff size={24} />
            </IconContainer>
            <NavRowText>Log Out</NavRowText>
          </NavRowContainer>
        </IsVisible>
      </LowerContainer>
    </NavBarOuterContainer>
  );
};

const NavBarOuterContainer = styled.div`
  display: flex;
  flex-direction: column;
  width: 200px;
  background-color: ${navBackground};
  border-right: 1px solid ${borderColor};
  z-index: 100;
`;

const LowerContainer = styled.div`
  margin-top: auto;
  padding-bottom: 20px;
`;

const AddProspectContainer = styled.div`
  display: flex;
  justify-content: space-between;
  height: 50px;
  margin-top: 10px;
  margin-bottom: 10px;
  padding-left: 10px;
  border-bottom: 1px solid ${borderColor};

`;

const UpperContainer = styled.main`
  display: flex;
  flex-direction: column;
  align-items: left;
  margin-top: 50px;
`;

const NavRowContainer = styled.div<NavRowContainerProps>`
  display: flex;
  flex-direction: row;
  align-items: center;
  margin: 0 10px;
  padding: 7px 5px;
  color: ${({ isSelected }) =>
    isSelected ? navbarTextSelectedColor : "black"};
  background-color: ${({ isSelected }) =>
    isSelected ? navBackgroundHover : "none"};
  border-radius: 5px;

  &:hover {
    color: ${navbarTextSelectedColor};
    background-color: ${navBackgroundHover};
    cursor: pointer;
  }
`;

const IconContainer = styled.div`
  margin-left: 20px;
  padding-bottom: 5px;
`;

const NavRowText = styled.div`
  margin-left: 10px;
  font-size: 16px;
`;

export default NavbarExpanded;
