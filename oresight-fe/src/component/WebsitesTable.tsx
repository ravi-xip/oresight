import React from 'react';
import { Table, Tag } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { Website } from '../shared/types';
import styled from 'styled-components';

type WebsitesTableProps = {
  websites: Website[];
};
const columns: ColumnsType<Website> = [
  {
    title: 'Name',
    dataIndex: 'name',
    key: 'name',
    width: 200,
    render: (text, record) => (
      <a href={record.url} target="_blank" rel="noopener noreferrer">
        {text}
      </a>
    )    
  },
  {
    title: 'Max Links',
    dataIndex: 'max_links',
    key: 'max_links',
    responsive: ['lg'],
    width: 150,  // fixed width of 150 pixels for the Max Links column
  },
  {
    title: '# Prospects',
    dataIndex: 'num_prospects',
    key: 'num_prospects',
    responsive: ['lg'],
    width: 150,  // fixed width of 150 pixels for the # Prospects column
  },
  {
    title: 'Status',
    dataIndex: 'status',
    key: 'status',
    responsive: ['lg'],
    width: 150,  // fixed width of 150 pixels for the Status column
    // ['PROCESSING', 'INDEXING', 'COMPLETED', 'FAILED']:
    render: (text) => {
      if (text.toUpperCase() === "PROCESSING") {
        return <Tag color="blue">{text}</Tag>;
      } else if (text.toUpperCase() === "INDEXING") {
        return <Tag color="yellow">{text}</Tag>;
      } else if (text.toUpperCase() === "COMPLETED") {
        return <Tag color="green">{text}</Tag>;
      } else {
        return <Tag color="red">{text}</Tag>;
      }
    }
  }
];

const WebsitesTable: React.FC<WebsitesTableProps> = ({ websites }) => {
  return (
    <TableContainer>
      <Table columns={columns} dataSource={websites} pagination={{ pageSize: 6 }}  />
    </TableContainer>
  );
};

const TableContainer = styled.div``;

export default WebsitesTable;