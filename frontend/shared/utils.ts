export const IsVisible = (props: { condition: boolean; children: any }) => {
    return props.condition ? props.children : null;
};
