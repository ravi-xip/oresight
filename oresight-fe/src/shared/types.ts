export type Website = {
    id: string;
    name: string;
    url: string;
    urlFilter: string;
    max_links: number;
    num_prospects: number;
    status: string;
    created_at: string;
    updated_at: string;
};

export type Prospect = {
    id: string;
    name: string;
    category: string;
    bio: string;
    url: string;
    email: string;
    phone: string;
    interest: string;
    website_id: string;
    created_at: string;
    updated_at: string;
};

export type Citation = {
    display_text: string;
    url: string;
};

export type Message = {
    // Indicates whether this piece of the conversation is by a bot or not.
    is_bot: boolean;
    // Actual text of the conversation.
    text: string;
    // Citations if any.
    citations?: Citation[];
};

export type Conversation = {
    messages: Message[];
};