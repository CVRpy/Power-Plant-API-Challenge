from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def calculate_power(load, fuels, powerplants):
    # Extract fuel costs
    gas_cost = fuels.get("gas(euro/MWh)")
    kerosine_cost = fuels.get("kerosine(euro/MWh)")
    wind_percentage = fuels.get("wind(%)")

    # Calculate power generation cost for gas-fired and turbojet powerplants
    for plant in powerplants:
        if plant['type'] == 'gasfired':
            plant['cost'] = gas_cost / plant['efficiency']
        elif plant['type'] == 'turbojet':
            plant['cost'] = kerosine_cost / plant['efficiency']
        else:
            plant['cost'] = 0  # Wind turbine

    # Sort powerplants by cost in ascending order
    powerplants.sort(key=lambda x: x['cost'])

    # Allocate power to each powerplant
    remaining_load = load
    result = []
    for plant in powerplants:
        if plant['type'] == 'windturbine':
            wind_power = min(plant['pmax'], load * wind_percentage / 100)
            result.append({"name": plant["name"], "p": wind_power})
            remaining_load -= wind_power
        else:
            pmax = min(plant['pmax'], remaining_load)
            pmin = plant['pmin']
            allocated_power = max(pmin, pmax)
            result.append({"name": plant["name"], "p": allocated_power})
            remaining_load -= allocated_power
        if remaining_load <= 0:
            break

    # Check if total allocated power matches the load
    total_allocated_power = sum(plant['p'] for plant in result)
    if abs(total_allocated_power - load) > 0.1:
        raise ValueError("Total allocated power does not match the load")

    return result

@app.route('/productionplan', methods=['POST'])
def production_plan():
    # Validate request content type
    if request.headers['Content-Type'] != 'application/json':
        return jsonify({"error": "Content-Type must be application/json"}), 400
    
    # Parse JSON payload
    try:
        data = request.json
    except:
        return jsonify({"error": "Invalid JSON payload"}), 400
    
    # Validate payload structure
    if 'load' not in data or 'fuels' not in data or 'powerplants' not in data:
        return jsonify({"error": "Payload must contain 'load', 'fuels', and 'powerplants'"}), 400
    
    # Validate load value
    load = data.get('load')
    if not isinstance(load, (int, float)) or load <= 0:
        return jsonify({"error": "'load' must be a positive number"}), 400

    # Validate fuels
    fuels = data.get('fuels')
    if not isinstance(fuels, dict) or 'gas(euro/MWh)' not in fuels or 'kerosine(euro/MWh)' not in fuels or 'wind(%)' not in fuels:
        return jsonify({"error": "'fuels' must contain 'gas(euro/MWh)', 'kerosine(euro/MWh)', and 'wind(%)'"}), 400
    
    # Validate powerplants
    powerplants = data.get('powerplants')
    if not isinstance(powerplants, list) or len(powerplants) == 0:
        return jsonify({"error": "'powerplants' must be a non-empty list"}), 400

    # Calculate production plan
    try:
        result = calculate_power(load, fuels, powerplants)
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888)
