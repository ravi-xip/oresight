import React from 'react';
import ReactMarkdown from 'react-markdown';
import LinkifyIt from 'linkify-it';

const linkify = LinkifyIt();

function linkifyText(text: string): string {
  const matches = linkify.match(text);
  if (!matches) return text;

  let lastIndex = 0;
  let result = '';

  matches.forEach((match: any) => {
    result += text.slice(lastIndex, match.index);
    result += `[${match.text}](${match.url})`;
    lastIndex = match.lastIndex;
  });

  result += text.slice(lastIndex);
  return result;
}

interface CustomMarkdownProps {
  text: string;
}

const CustomMarkdown: React.FC<CustomMarkdownProps> = ({ text }) => {
  const linkifiedText = text;
  return <ReactMarkdown>{linkifiedText}</ReactMarkdown>;
}

export default CustomMarkdown;
