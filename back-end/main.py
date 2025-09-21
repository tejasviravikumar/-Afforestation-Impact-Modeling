from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import json
import os
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
import io
from typing import Dict, List, Optional

app = FastAPI(title="Tree Dashboard API", version="1.0.0")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# File paths
TREE_DATA_FILE = "data/tree-species.json"
GRAPHS_DIR = "graphs"

# Ensure graphs directory exists
os.makedirs(GRAPHS_DIR, exist_ok=True)

def load_tree_data():
    """Load tree species data from JSON file"""
    try:
        with open(TREE_DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Tree species data file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON format")

def create_co2_total_graph(tree_data: Dict, selected_trees: Optional[Dict[str, int]] = None):
    """Generate bar graph showing total CO2 per species over 20 years"""
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 8))
    
    species_names = []
    co2_values = []
    
    # If specific trees are selected, use only those; otherwise use all
    trees_to_plot = selected_trees if selected_trees else {name: 1 for name in tree_data.keys()}
    
    for tree_name, quantity in trees_to_plot.items():
        if tree_name in tree_data:
            # Get the last value from CO2_years array (20-year total)
            co2_20yr = tree_data[tree_name].get("CO2_years", [0])[-1]
            total_co2 = co2_20yr * quantity
            
            species_names.append(tree_name)
            co2_values.append(total_co2)
    
    # Create bar chart
    bars = ax.bar(species_names, co2_values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                                                   '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'])
    
    # Customize chart
    ax.set_title('Total CO₂ Sequestration per Species (20 Years)', fontsize=16, fontweight='bold', color='white')
    ax.set_xlabel('Tree Species', fontsize=12, color='white')
    ax.set_ylabel('CO₂ Sequestered (kg)', fontsize=12, color='white')
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right', color='white')
    plt.yticks(color='white')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                f'{height:.1f}', ha='center', va='bottom', color='white', fontweight='bold')
    
    # Improve layout
    plt.tight_layout()
    
    return fig

def create_co2_yearly_graph(tree_data: Dict, selected_trees: Optional[Dict[str, int]] = None):
    """Generate line graph showing yearly CO2 accumulation for multiple species"""
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(14, 8))
    
    years = list(range(1, 21))  # 1 to 20 years
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
              '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    trees_to_plot = selected_trees if selected_trees else {name: 1 for name in tree_data.keys()}
    
    color_idx = 0
    for tree_name, quantity in trees_to_plot.items():
        if tree_name in tree_data and color_idx < len(colors):
            co2_years = tree_data[tree_name].get("CO2_years", [0] * 20)
            
            # Scale by quantity
            scaled_co2 = [co2 * quantity for co2 in co2_years]
            
            ax.plot(years, scaled_co2, marker='o', linewidth=2.5, markersize=4, 
                   label=f'{tree_name} (x{quantity})', color=colors[color_idx])
            color_idx += 1
    
    # Customize chart
    ax.set_title('Yearly CO₂ Accumulation by Species', fontsize=16, fontweight='bold', color='white')
    ax.set_xlabel('Years', fontsize=12, color='white')
    ax.set_ylabel('Cumulative CO₂ Sequestered (kg)', fontsize=12, color='white')
    
    # Add grid and legend
    ax.grid(True, alpha=0.3)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', facecolor='black', edgecolor='white')
    
    # Style axes
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    
    plt.tight_layout()
    
    return fig

def create_survival_rate_graph(tree_data: Dict, selected_trees: Optional[Dict[str, int]] = None):
    """Generate bar graph showing survival rates as percentages"""
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 8))
    
    species_names = []
    survival_rates = []
    
    trees_to_plot = selected_trees if selected_trees else tree_data.keys()
    
    for tree_name in trees_to_plot:
        if tree_name in tree_data:
            survival_rate = tree_data[tree_name].get("Survival_Rate", 0) * 100
            species_names.append(tree_name)
            survival_rates.append(survival_rate)
    
    # Create bar chart with color coding based on survival rate
    colors = []
    for rate in survival_rates:
        if rate >= 80:
            colors.append('#2ca02c')  # Green for high survival
        elif rate >= 60:
            colors.append('#ff7f0e')  # Orange for medium survival
        else:
            colors.append('#d62728')  # Red for low survival
    
    bars = ax.bar(species_names, survival_rates, color=colors)
    
    # Customize chart
    ax.set_title('Tree Species Survival Rates', fontsize=16, fontweight='bold', color='white')
    ax.set_xlabel('Tree Species', fontsize=12, color='white')
    ax.set_ylabel('Survival Rate (%)', fontsize=12, color='white')
    
    # Set y-axis to show 0-100%
    ax.set_ylim(0, 100)
    
    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right', color='white')
    plt.yticks(color='white')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', color='white', fontweight='bold')
    
    # Add legend for colors
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='#2ca02c', label='High (≥80%)'),
                      Patch(facecolor='#ff7f0e', label='Medium (60-79%)'),
                      Patch(facecolor='#d62728', label='Low (<60%)')]
    ax.legend(handles=legend_elements, loc='upper right', facecolor='black', edgecolor='white')
    
    # Style axes
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    
    plt.tight_layout()
    
    return fig

def fig_to_response(fig):
    """Convert matplotlib figure to HTTP response"""
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight', 
                facecolor='black', edgecolor='none')
    img_buffer.seek(0)
    plt.close(fig)  # Free memory
    
    return StreamingResponse(
        io.BytesIO(img_buffer.getvalue()), 
        media_type="image/png",
        headers={"Cache-Control": "no-cache"}
    )

@app.get("/")
async def root():
    return {"message": "Tree Dashboard API", "status": "running"}

@app.get("/graph/co2_total")
async def get_co2_total_graph(species: Optional[str] = None):
    """Get total CO2 bar chart. Optional: filter by species (comma-separated)"""
    tree_data = load_tree_data()
    
    selected_trees = None
    if species:
        # Parse comma-separated species list
        species_list = [s.strip() for s in species.split(',')]
        selected_trees = {name: 1 for name in species_list if name in tree_data}
        
        if not selected_trees:
            raise HTTPException(status_code=400, detail="No valid species found")
    
    fig = create_co2_total_graph(tree_data, selected_trees)
    return fig_to_response(fig)

@app.get("/graph/co2_yearly")
async def get_co2_yearly_graph(species: Optional[str] = None, years: Optional[int] = 20):
    """Get yearly CO2 line chart. Optional: filter by species and years"""
    tree_data = load_tree_data()
    
    selected_trees = None
    if species:
        species_list = [s.strip() for s in species.split(',')]
        selected_trees = {name: 1 for name in species_list if name in tree_data}
        
        if not selected_trees:
            raise HTTPException(status_code=400, detail="No valid species found")
    
    # Limit years if specified
    if years and years < 20:
        # Truncate CO2_years data for each species
        for tree_name in tree_data:
            if len(tree_data[tree_name].get("CO2_years", [])) > years:
                tree_data[tree_name]["CO2_years"] = tree_data[tree_name]["CO2_years"][:years]
    
    fig = create_co2_yearly_graph(tree_data, selected_trees)
    return fig_to_response(fig)

@app.get("/graph/survival")
async def get_survival_rate_graph(species: Optional[str] = None):
    """Get survival rate bar chart. Optional: filter by species (comma-separated)"""
    tree_data = load_tree_data()
    
    selected_trees = None
    if species:
        species_list = [s.strip() for s in species.split(',')]
        selected_trees = species_list
        
        # Validate species exist
        valid_species = [name for name in species_list if name in tree_data]
        if not valid_species:
            raise HTTPException(status_code=400, detail="No valid species found")
        selected_trees = valid_species
    
    fig = create_survival_rate_graph(tree_data, selected_trees)
    return fig_to_response(fig)

@app.post("/graph/generate_dashboard")
async def generate_dashboard(selected_trees: Dict[str, int]):
    """Generate all three graphs based on selected trees from frontend"""
    tree_data = load_tree_data()
    
    # Validate selected trees
    valid_trees = {name: qty for name, qty in selected_trees.items() if name in tree_data}
    
    if not valid_trees:
        raise HTTPException(status_code=400, detail="No valid tree species found in selection")
    
    # Save graphs to files for later retrieval
    graphs_info = {}
    
    try:
        # Generate CO2 total graph
        fig1 = create_co2_total_graph(tree_data, valid_trees)
        co2_total_path = os.path.join(GRAPHS_DIR, "co2_total.png")
        fig1.savefig(co2_total_path, dpi=300, bbox_inches='tight', facecolor='black')
        plt.close(fig1)
        graphs_info["co2_total"] = "/graph/co2_total"
        
        # Generate yearly CO2 graph
        fig2 = create_co2_yearly_graph(tree_data, valid_trees)
        co2_yearly_path = os.path.join(GRAPHS_DIR, "co2_yearly.png")
        fig2.savefig(co2_yearly_path, dpi=300, bbox_inches='tight', facecolor='black')
        plt.close(fig2)
        graphs_info["co2_yearly"] = "/graph/co2_yearly"
        
        # Generate survival rate graph
        fig3 = create_survival_rate_graph(tree_data, list(valid_trees.keys()))
        survival_path = os.path.join(GRAPHS_DIR, "survival.png")
        fig3.savefig(survival_path, dpi=300, bbox_inches='tight', facecolor='black')
        plt.close(fig3)
        graphs_info["survival"] = "/graph/survival"
        
        return {
            "success": True,
            "message": "Dashboard generated successfully",
            "graphs": graphs_info,
            "total_trees": sum(valid_trees.values()),
            "species_count": len(valid_trees)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating graphs: {str(e)}")

@app.get("/data/species")
async def get_species_list():
    """Get list of available tree species"""
    tree_data = load_tree_data()
    return {"species": list(tree_data.keys())}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)