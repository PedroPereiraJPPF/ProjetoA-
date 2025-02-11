
class GraphDrawer {
    constructor(containerId, data) {
        this.container = document.getElementById(containerId);
        this.nodes = new vis.DataSet(data.nodes);
        this.edges = new vis.DataSet(data.edges);
        this.network = null;
        this.render();
    }

    render() {
        let data = { nodes: this.nodes, edges: this.edges };
        let options = { physics: { enabled: true }, edges: { arrows: "to" } };
        this.network = new vis.Network(this.container, data, options);
    }

    addNode(id, label) {
        this.nodes.add({ id, label });
    }

    addEdge(from, to) {
        this.edges.add({ from, to });
    }
}

const data = {
    nodes: [{ id: 1, label: "A" }, { id: 2, label: "B" }, { id: 3, label: "C" }],
    edges: [{ from: 1, to: 2 }, { from: 2, to: 3 }]
};

const graph = new GraphDrawer("mynetwork", data);

setTimeout(() => {
    graph.addNode(4, "D");
    graph.addEdge(3, 4);
}, 2000);

export default GraphDrawer;
