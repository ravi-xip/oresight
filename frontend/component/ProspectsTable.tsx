import React from 'react';
import { Table, Tag } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { Prospect } from '../shared/types';
import styled from 'styled-components';

type ProspectsTableProps = {
  prospects: Prospect[];
};
const columns: ColumnsType<Prospect> = [
  {
    title: 'Name',
    dataIndex: 'name',
    key: 'name',
    width: 200,
    sorter: (a: Prospect, b: Prospect) => a.name.localeCompare(b.name), // sort by alphabets
    render: (text, record) => (
      <a href={record.url} target="_blank" rel="noopener noreferrer">
        {text}
      </a>
    )
  },
  {
    title: 'Bio',
    dataIndex: 'bio',
    key: 'bio',
    width: 800,
    sorter: (a: Prospect, b: Prospect) => a.bio.length - b.bio.length, // sort by length
  },
  {
    title: 'Category',
    dataIndex: 'category',
    key: 'category',
    sorter: (a: Prospect, b: Prospect) => {
      if (a.category === b.category) {
        return 0;
      } else if (a.category.toUpperCase() === "STUDENT") {
        return -1;
      } else if (b.category.toUpperCase() === "STUDENT") {
        return 1;
      } else if (a.category.toUpperCase() === "INSTRUCTOR") {
        return -1;
      } else {
        return 1;
      }
    },
    render: (text) => {
      if (text.toUpperCase() === "STUDENT") {
        return <Tag color="blue">{text}</Tag>;
      } else if (text.toUpperCase() === "INSTRUCTOR") {
        return <Tag color="green">{text}</Tag>;
      } else {
        return <Tag color="red">{text}</Tag>;
      }
    }
  }
];


const ProspectsTable: React.FC<ProspectsTableProps> = ({ prospects }) => {
  return (
    <TableContainer>
      <Table columns={columns} dataSource={prospects} pagination={{ pageSize: 7 }} />
    </TableContainer>
    );
};

const TableContainer = styled.div`
  height: 80vh;
`;

export default ProspectsTable;
