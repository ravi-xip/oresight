import { Button, Modal, notification } from 'antd';
import { NotificationPlacement } from 'antd/es/notification/interface';
import React, { useState } from 'react';
import styled from 'styled-components';
import { axiosSimple } from '../shared/axios';
import { Config } from '../shared/config';

const StyledModal = styled.div < { open: boolean } > `
  display: ${props => (props.open ? 'block' : 'none')};
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80%;
  max-width: 600px;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  font-family: 'Roboto', sans-serif;
`;

const StyledForm = styled.form`
  display: flex;
  flex-direction: column;
  gap: 15px;
`;

const StyledLabel = styled.label`
  display: flex;
  flex-direction: column;
  font-weight: 500;
`;

const StyledInput = styled.input`
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
  font-size: 14px;
  transition: border-color 0.3s;

  &:focus {
    border-color: #0077cc;
    outline: none;
  }
`;

const ButtonContainer = styled.div`
    display: flex;
    flex-direction: row;
    justify-content: flex-end;
    gap: 10px;
`;

const Title = styled.h1`
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 10px;
`;

const AddProspectButton = styled(Button)`
  background-color: transparent;
  color: black;
  border-radius: 5px;
  font-size: 12px;
  font-weight: 300;
  border: 1px solid black;
  box-shadow: 0px 0px 0px 0px #1a75ff;

  &:hover {
    background-color: #e0e0e0;
    color: black;
  }
`;

const WebsiteModal = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [api, contextHolder] = notification.useNotification();
  
  const [formData, setFormData] = useState({
    websiteName: '',
    websiteURL: '',
    maxLinks: ''
  });

  const openNotification = (placement: NotificationPlacement, message: string) => {
    api.info({
      message: message,
      description: 'This website has been added to the list of websites to be indexed.',
      placement,
    });
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleOk = () => {
    const url = Config.getMasterUrl() + '/api/v1/websites';
    axiosSimple
        .post(url, {
            name: formData.websiteName,
            url: formData.websiteURL,
            max_links: formData.maxLinks,
            url_filter: "comments"
        })
        .then((response) => {
            console.log(response);
            // Refresh the page
            window.location.reload();
            // Show a notification to the user
            openNotification('top', response.data.message);
        })
        .catch((error) => {
            console.log(error);
        });
    
    setIsModalOpen(false);
  };

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  return (
    <>
      <StyledModal open={isModalOpen}>
        <Title>Add Prospects</Title>
        <StyledForm> 
          <StyledLabel>
            <StyledInput
              type="text"
              name="websiteName"
              value={formData.websiteName}
              onChange={handleInputChange}
              placeholder="Website Name"
            />
          </StyledLabel>
          <StyledLabel>
            <StyledInput
              type="url"
              name="websiteURL"
              value={formData.websiteURL}
              onChange={handleInputChange}
              placeholder="Url ..."
            />
          </StyledLabel>
          <StyledLabel>
            <StyledInput
              type="number"
              name="maxLinks"
              value={formData.maxLinks}
              onChange={handleInputChange}
              placeholder="Max Links ..."
            />
          </StyledLabel>
          <ButtonContainer>
            <Button type="primary" onClick={handleOk}> Done </Button>
            <Button type="primary" onClick={handleCancel}> Cancel </Button>
        </ButtonContainer>
        </StyledForm>
      </StyledModal>
      <AddProspectButton onClick={() => setIsModalOpen(true)}> + Add Prospect</AddProspectButton>
    </>
  );
}

export default WebsiteModal;
