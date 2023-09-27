import React from "react";
import { styled } from "styled-components";
import ReactMarkdown from "react-markdown";
import CustomMarkdown from "./CustomMarkdown";

type BotComponentProps = {
    text: string;
    is_bot?: boolean;
    img_src?: string;
    user_name?: string;
};

const MainContainer = styled.div<{ is_bot?: boolean }>`
    display: flex;
    flex-direction: row;
    padding-top: 10px;
    width: 100%;
    box-sizing: border-box;
    background-color: ${props => props.is_bot ? "#fffafa" : "white"};
`;

const InnerContainer = styled.div`
    display: flex;
    flex-direction: row;
    width: 600px;
    height: 100%;
    position: relative;
    left: 30%;
    
`;

const ImageContainer = styled.div`
    width: 50px;
    height: 50px;
    margin-top: 5px;    
`;

const ResponseContainer = styled.div`
    font-size: 13px;
    line-height: 1.5;
    width: 600px;
`;

const MessageBlock: React.FC<BotComponentProps> = ({ text, is_bot }) => {
    return (
        <MainContainer is_bot={is_bot}>
            <InnerContainer>
                <ImageContainer>
                    {is_bot ? <img src="/favicon.png" width="30px" height="30px" /> : null}
                    {!is_bot ? <img src="/face.png" width="30px" height="30px" /> : null}
                </ImageContainer>
                <ResponseContainer>
                    <CustomMarkdown text={text} />
                </ResponseContainer>
            </InnerContainer>
        </MainContainer>
    )
};

export default MessageBlock;
