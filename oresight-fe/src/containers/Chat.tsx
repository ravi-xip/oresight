import { SendOutlined, StarFilled, SyncOutlined } from '@ant-design/icons';
import React, { useEffect } from 'react';
import styled from 'styled-components';
import MessageBlock from '../component/MessageBlock';
import { axiosSimple } from '../shared/axios';
import { Config } from '../shared/config';
import { Message } from '../shared/types';
import { IsVisible } from '../shared/utils';

const MainContainer = styled.div`
  display: flex;
  flex-direction: column;
  margin: 0 0;
`;

const TopNavbar = styled.div`
  display: flex;
  flex-direction: row;
  height: 50px;
  color: black;
  align-items: center;
  font-size: 12px;
  background-color: white;
  border-bottom: 0.5px solid #ccc;
  font-family: 'Roboto', sans-serif;
  font-weight: 350;
  letter-spacing: 1px;
  padding-left: 40%;
`;

const NavIcon = styled.div`
  margin-right: 5px;
`;

const NavText = styled.div``;

const SearchContainer = styled.div`
  position: fixed;
  bottom: 30px;
  max-width: 600px;
  height: 50px;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  padding: 0 5px;
`;

const StickyInput = styled.input`
  flex: 1;
  padding: 10px;
  box-sizing: border-box;
  border: none;
  height: 100%;

  &:focus {
    outline: none;
  }
`;

const SendIconContainer = styled.div`
  padding: 5px;
  color: black;
  cursor: pointer;
  width: 20px;

  &:hover {
    color: #1890ff;
  }
`;

const ResultContainer = styled.div`
  bottom: 100px;
  padding-bottom: 100px;  
`;

const OuterContainer = styled.div`
  display: flex;
  flex-direction: column;
`;

const DummyElement = styled.div`
  width: 100%;
  height: 1px;
`;

// Enable test mode
const ENABLE_TEST_MODE = false;

// Generate dummy data for conversations
const message_bot = {
  text: 'Hello! I am OreSight - your one stop solution for your prospecting needs.',
  is_bot: true,
};

const message_user = {
  text: 'Share some good prospects for Basketball',
  is_bot: false,
};

const Chat: React.FC<{}> = ({  }) => {
  const [query, setQuery] = React.useState<string>('');
  const [conversation, setConversation] = React.useState<Message[]>([]);
  const [searchInProgress, setSearchInProgress] = React.useState<boolean>(false);


  // Scroll to the bottom of the page.
  const scrollToBottom = () => {
    var scrollableElement = document.body;
    scrollableElement.scrollTop = scrollableElement.scrollHeight;
    console.log('Scrolling to the bottom')

    const element = document.getElementById("dummy-element");
      if (element) {
        console.log('Bringing the dummy element into view')
        element.scrollIntoView({ behavior: "smooth", block: "end" });
    }
  };

  useEffect(() => {
    // Step I: Add the bot message to the conversation
    setConversation((prevConversation) => [...prevConversation, message_bot]);

    if (ENABLE_TEST_MODE) {
      // Step II: Add the user message to the conversation
      setConversation((prevConversation) => [...prevConversation, message_user]);

      // Step III: Add an answer from the bot to the conversation.
      // This is just to test the UI
      // Generate a markdown with links in it
      const message_bot_2 = {
        // Generate a markdown with links in it
        text: "Here's a list of prospects for Basketball \n\n [Prospect 1](https://www.google.com) \n\n [Prospect 2](https://www.google.com) \n\n [Prospect 3](https://www.google.com)",
        is_bot: true,
      };
      setConversation((prevConversation) => [...prevConversation, message_bot_2]);
    }
  }, []);

  const handleSearch = async (text: string) => {
    // Step I: Clear the input
    setQuery('');
    
    // Step II: Make the input disabled till the query is being fetched 
    setSearchInProgress(true);
    
    // Step III: Add the query to the conversation
    // Because this is a user query, the is_bot flag is set to false
    setConversation((prevConversation) => [
      ...prevConversation,
      {
        text: text,
        is_bot: false,
      },
    ]);
    
   // Step III (b): Go through the last two messages (one is the query and the other is the bot response) create a conversation object
   const lastTwoMessages = conversation.slice(-2);
   // Extract the text as a string
  const lastTwoMessagesText = lastTwoMessages.map((message) => message.text).join('\n\n');
  // Ensure that the text is encoded
  const lastTwoMessagesTextEncoded = encodeURIComponent(lastTwoMessagesText);

    // Step IV: Trigger a GET request to the backend
    const url = Config.getMasterUrl() + '/api/v1/chat?query=' + text + '&conversation=' + lastTwoMessagesTextEncoded;
    const response = await axiosSimple.get(url);
    
    // Step V: Once the response is received, add it to the conversation
    const responseData = response.data;
    const responseText = responseData.text;
    const responseLink = responseData.link;
    setConversation((prevConversation) => [
      ...prevConversation,
      {
        text: responseText,
        is_bot: true,
      },
    ]);    
    
    // Step VII: If the response has a link, add it to the conversation
    console.log('Searching with the query ', text);

    // Step N: Last step is to enable the input again, once the search is complete
    setSearchInProgress(false);

    // Step VIII: Scroll to the bottom of the page
    scrollToBottom();
  };

  return (
    <MainContainer>
      <TopNavbar>
        <NavIcon><StarFilled /></NavIcon>
        <NavText>OreSight</NavText>
      </TopNavbar>
      <OuterContainer>
        <ResultContainer>
          {conversation.map((message, index) => {
            return (
              <div key={index}>
                {message.is_bot ? (
                  <div>
                    <MessageBlock text={message.text} is_bot={true} />
                  </div>
                ) : (
                  <div>
                    <MessageBlock text={message.text} is_bot={false} />
                  </div>
                )}
              </div>
            );
          })}
          <DummyElement id="dummy-element" />
        </ResultContainer>
        <SearchContainer>
        <StickyInput
          type="text"
          placeholder="Send a message"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          disabled={searchInProgress}
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              handleSearch(e.currentTarget.value);
            }
          }}
        />
        <IsVisible condition = {searchInProgress}>
          <SyncOutlined spin style = {{marginRight: "10px"}} />
        </IsVisible>
        <SendIconContainer onClick={() => handleSearch(query)}>
          <SendOutlined />
        </SendIconContainer>
      </SearchContainer>
    </OuterContainer>
    </MainContainer>
  );
}

export default Chat;
