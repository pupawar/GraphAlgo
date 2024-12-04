
  <template>
    <div class ="graph-container">
      <div class="button-bar">
        <button @click="addNode">Add Node</button>
        <Button :disabled="selectedNodes.length!=2" @click="addEdge">Add Edge</Button>
        <Button @click="deleteEdge">Remove Edge</Button>
        <Button :disabled="selectedNodes.length !=1" @click="deleteNode">Remove Node</Button>
        <Button @click="saveGraph">Save</Button>
        <input :disabled="selectedEdge.length !=1" v-model="weight" @keydown.enter="editWeight" placeholder="Weight" />

      </div>
      <v-network-graph :nodes="nodes.value" :edges="edges.value" :configs="configs" v-model:selected-nodes="selectedNodes" v-model:selected-edges="selectedEdge" :event-handler="eventHandlers">

        <template #edge-label="{ edge, hovered, selected, ...slotProps }">
        <v-edge-label
          :class="{ hovered, selected }"
          :text="edge.label"
          align="center"
          vertical-align="above"
          v-bind="slotProps"
        />
        </template>
      </v-network-graph>
    </div>

  </template>

  <script setup >
    import { defineConfigs } from "v-network-graph";
    import {reactive, ref, watch, onBeforeMount} from "vue";

    // import * as vNG from "v-network-graph"

    const configs = defineConfigs({
      node: {
        selectable: 2 
      },
      edge: {
        selectable: true,
        hoverable: true, 
        label: {
          fontSize: 11,
          color: "#000000",
        },
      }
    });
    
    const API_URL = process.env.VUE_APP_API_ROUTE;

    let nodes = reactive({});

    let edges = reactive({});

  const selectedNodes = ref([]);
  const selectedEdge = ref([]);
  const nextNodeIndex = ref(0);
  const nextEdgeIndex = ref(0);
  const weight = ref('');
  // const eventHandlers  = {
  //   "edge:dblclick": (edgeKey) =>{ 
  //     console.log('hi');
  //     editLabel(edgeKey)}


  // }
  const eventHandlers = {
    '*': (eventName, edgeKey) => {
      console.log(`Event: ${eventName}`, edgeKey);
    },
  };

  onBeforeMount(async () => {
    try {
      console.log(`${API_URL}`);
      const response = await fetch(`${API_URL}/get-graph`);
      const data = await response.json();

      nodes.value = data.nodes;
      edges.value = data.edges;
      nextNodeIndex.value = Object.keys(nodes.value).length + 1;
      nextEdgeIndex.value = Object.keys(edges.value).length + 1
    
    } catch (error) {
      console.error(error);
    }
  });

  // function editLabel(edgeKey){
  //   console.log(edges[edgeKey]);
  //   console.log(selectedEdge.value[0])
  // }

  function addNode(){
    const newNode = nextNodeIndex.value;
    const name = `Node ${nextNodeIndex.value}`;
    nodes.value[newNode] = {name};
    nextNodeIndex.value++;
  }

  function addEdge(){
    edges.value[`edge${nextEdgeIndex.value}`] = {source: selectedNodes.value[0], target: selectedNodes.value[1], label: '1'}
    nextEdgeIndex.value++;
  }

  watch(selectedNodes, (newValue) => {
    console.log("Selected Nodes:", newValue);
  });

  function editWeight(){
    edges.value[selectedEdge.value[0]].label = weight.value;
    weight.value = '';
  }
  function deleteEdge(){
    delete edges.value[selectedEdge.value[0]];
  }


  function deleteNode(){
    Object.keys(edges.value).forEach(key => {
      if(edges.value[key].target == selectedNodes.value[0] || edges.value[key].source == selectedNodes.value[0] ){
        delete edges.value[key];
      }
    });
    delete nodes.value[selectedNodes.value[0]];
  }

  </script>


<style scoped>
.button-bar {
  display: flex; /* Arrange buttons horizontally */
  justify-content: center; /* Center buttons horizontally */
  gap: 10px; /* Add spacing between buttons */
  padding: 10px; /* Add some space around the buttons */
  background-color: #e8e8e8; /* Optional: background color for the button bar */
  width: 100%; /* Make the button bar span the full width */
  border-bottom: 2px solid #ccc; /* Optional: border below the button bar */
  box-sizing: border-box; /* Include padding and border in element's total width */
}

.graph-container {
  width: 600px; /* Set desired width */
  height: 400px; /* Set desired height */
  border: 2px solid #2c3e50; /* Add a border to simulate a rectangular canvas */
  border-radius: 8px; /* Optional: rounded corners */
  background-color: #f9f9f9; /* Optional: background color for the canvas */
  margin: auto; /* Center the container horizontally */
  display: flex; /* Center the content inside the container */
  align-items: center; /* Center the graph vertically */
  justify-content: center; /* Center the graph horizontally */
  flex-direction: column;

}
.v-ng-edge-label {
  transition: fill 0.1s;
}
.v-ng-edge-label.hovered {
  fill: #3355bb;
  font-weight: bold;
}
.v-ng-edge-label.selected {
  fill: #dd8800;
  font-weight: bold;
}
</style>