import React, { useState } from "react";
import styled from "styled-components";
import { IsVisible } from "../../shared/utils";
import NavbarCollapsed from "./NavbarCollapsed";
import NavbarExpanded from "./NavbarExpanded";

const Navbar: React.FC = (): JSX.Element => {
  const [showLeftPanel, setShowLeftPanel] = useState<boolean>(false);

  return (
    <>
      <IsVisible condition={showLeftPanel}>
        <NavbarExpanded setShowLeftPanel={setShowLeftPanel} />
      </IsVisible>
      <IsVisible condition={!showLeftPanel}>
        <NavbarCollapsed setShowLeftPanel={setShowLeftPanel} />
      </IsVisible>
    </>
  );
};

export const HamburgerMenuContainer = styled.div`
  width: 100px;
  border-radius: 0 10px 10px 0;
  margin-left: 10px;
  padding-top: 5px;
  z-index: 100;

  &:hover {
    cursor: pointer;
  }
`;

export default Navbar;
