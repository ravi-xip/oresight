
declare const ENV: {
    development?: boolean;
    production?: boolean;
    staging?: boolean;
    swapnildev?: boolean;
};

export class Config {
    static getMasterUrl = () => {        
        // Default is development.
        return "https://ravi-xip.ngrok.io/backend/";
    };
};