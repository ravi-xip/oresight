import React from 'react';
import WebsitesTable from '../component/WebsitesTable';
import { axiosSimple } from '../shared/axios';
import { Config } from '../shared/config';
import { Prospect, Website } from '../shared/types';
import { Tabs } from 'antd';
import styled from 'styled-components';
import ProspectsTable from '../component/ProspectsTable';

const Home: React.FC = () => {
    const [websites, setWebsites] = React.useState<Website[]>([]);
    const [prospects, setProspects] = React.useState<Prospect[]>([]);
    const [activeTab, setActiveTab] = React.useState<string>("1");
    const [isModalOpen, setIsModalOpen] = React.useState(false);

    const onChange = (key: string) => {
        console.log(key);
        setActiveTab(key);
      };

      
    React.useEffect(() => {
        // Step I: Get all the websites
        axiosSimple(Config.getMasterUrl() + "/api/v1/websites")
        .then((response) => {  
            setWebsites(response.data);            
        })
        .catch((error) => {
            console.log(error);
        });

        // Step II: Get all the prospects
        axiosSimple(Config.getMasterUrl() + "/api/v1/prospects")
        .then((response) => {
            console.log(response);
            setProspects(response.data);
        })
        .catch((error) => {
            console.log(error);
        });
    }, []);

    const getTabLabel = (id: string) => {
        if (id === "1") {
            return "Websites";
        } else if (id === "2") {
            return "Prospects";
        } else {
            return "Unknown";
        }
    };

    return (
        <HomeContainer>
            <TableContainer>
            <Tabs
                onChange={onChange}
                type="card"
                items={new Array(2).fill(null).map((_, i) => {
                const id = String(i + 1);
                return {
                    label: getTabLabel(id),
                    key: id,                    
                    children: id === "1" ? <WebsitesTable websites={websites} /> : <ProspectsTable prospects={prospects} />
                };
            })}
            >
            </Tabs>
            </TableContainer>
        </HomeContainer>
    );
};

const HomeContainer = styled.div`
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100vh;
`;

const TableContainer = styled.div`
    display: flex;
    flex-direction: column;
    width: 1000px;
    top: 10px;
    height: 60vh;
    box-shadow: 0 1px 2px 0 rgba(0,0,0,.05);
    background-color: #fff;
    left: 300px;
    position: absolute;
`;

export default Home;