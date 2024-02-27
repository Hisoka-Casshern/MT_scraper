"""Here we define the ship type Hierarchy that will be used
to filter out and augment data"
"Data is defined on MarineTraffic.com based on AIS message"
"Ship types hierarchy and augmented further for similar typing,
 format: General Type: Ship Type: Ship Type Specific"""

shipTypeHierarchy: dict[str : dict[str : list[str]]] = {
    "WING IN GRND": {"WING IN GRND": ["WING IN GRND", "WING IN GROUND EFFECT VESSEL"]},
    "FISHING": {
        "FISHING": [
            "FISHING",
            "FISHING VESSEL",
            "TRAWLER",
            "FISHERY PROTECTION/RESEARCH",
            "FISH CARRIER",
            "FISH FACTORY",
            "FACTORY TRAWLER",
            "FISH STORAGE BARGE",
            "FISHERY RESEARCH VESSEL",
            "FISHERY PATROL VESSEL",
            "FISHERY SUPPORT VESSEL",
            "INLAND, FISHING BOAT",
        ]
    },
    "TUG": {
        "TUG": [
            "TUG",
            "TOWING VESSEL",
            "TUG/TENDER",
            "TUG/SUPPLY VESSEL",
            "TUG/FIRE FIGHTING VESSEL",
            "TUG/PILOT SHIP",
            "ANCHOR HANDLING SALVAGE TUG",
            "TOWING/PUSHING",
            "TUG/ICE BREAKER",
            "TRACTOR TUG",
            "TUG/SUPPORT",
            "ARTICULATED PUSHER TUG",
            "ICEBREAKER",
            "INLAND TUG",
            "PUSHER TUG",
        ]
    },
    "SPECIAL CRAFT": {
        "DREDGER": [
            "SUCTION HOPPER DREDGER",
            "DREDGER",
            "DRILL SHIP",
            "GRAB HOPPER DREDGER",
            "GRAB DREDGER",
            "SAND SUCTION DREDGER",
            "HOPPER DREDGER",
            "CUTTER SUCTION DREDGER",
            "CUTTER SUCTION HOPPER DREDGER",
            "SUCTION DREDGER",
            "BUCKET DREDGER",
            "TRAILING SUCTION HOPPER DREDGE",
            "TRAILING SUCTION DREDGER",
            "INLAND DREDGER",
            "DRILLING JACK UP",
            "BUCKET LADDER DREDGER",
            "DRILL BARGE",
            "BUCKET HOPPER DREDGER",
            "BUCKET DREDGER PONTOON",
            "BUCKET WHEEL SUCTION DREDGER",
            "DREDGING PONTOON",
            "BACKHOE DREDGER",
            "SUCTION DREDGER PONTOON",
            "WATER JET DREDGING PONTOON",
            "GRAB DREDGER PONTOON",
            "KELP DREDGER",
        ],
        "DIVE VESSEL": ["DIVING SUPPORT VESSEL"],
        "MILITARY OPS": [
            "MILITARY OPS",
            "NAVAL/NAVAL AUXILIARY VESSEL",
            "NAVAL AUXILIARY TUG",
            "LOGISTICS NAVAL VESSEL",
            "MINE HUNTER",
            "MINESWEEPER",
            "COMBAT VESSEL",
            "COMMAND VESSEL",
            "NAVAL SALVAGE VESSEL",
            "TORPEDO RECOVERY VESSEL",
            "NAVAL RESEARCH VESSEL",
            "NAVAL PATROL VESSEL",
            "TROOPSHIP",
            "RADAR VESSEL",
        ],
        "PILOT VESSEL": ["PILOT VESSEL"],
        "PORT TENDER": [
            "PORT TENDER",
            "TENDER",
            "CREW BOAT",
            "PILOT SHIP",
            "SUPPLY TENDER",
        ],
        "ANTI-POLLUTION": ["ANTI-POLLUTION", "POLLUTION CONTROL VESSEL"],
        "LAW ENFORCE": ["LAW ENFORCE", "PATROL VESSEL"],
        "LOCAL VESSEL": ["LOCAL VESSEL"],
        "MEDICAL TRANS": ["MEDICAL TRANS", "HOSPITAL SHIP"],
        "SPECIAL CRAFT": [
            "SPECIAL CRAFT",
            "MULTI PURPOSE OFFSHORE VESSEL",
            "BARGE CARRIER",
            "HEAVY LIFT VESSEL",
            "SPECIAL VESSEL",
            "MAINTENANCE VESSEL",
            "PIPE LAYER",
            "WASTE DISPOSAL VESSEL",
            "SUPPLY VESSEL",
            "TRAINING SHIP",
            "FLOATING STORAGE/PRODUCTION",
            "RADIO SHIP",
            "RESEARCH/SURVEY VESSEL",
            "REPAIR SHIP",
            "SUPPORT VESSEL",
            "FIRE FIGHTING TRACTOR TUG",
            "LANDING CRAFT",
            "FLOATING CRANE",
            "FIRE FIGHTING/SUPPLY VESSEL",
            "WHALER",
            "MULTI-PURPOSE VESSEL",
            "TANK-CLEANING VESSEL",
            "MINING VESSEL",
            "FIRE FIGHTING VESSEL",
            "PADDLE SHIP",
            "ANCHOR HANDLING VESSEL",
            "NUCLEAR FUEL CARRIER",
            "SLUDGE CARRIER",
            "WHALE FACTORY",
            "UTILITY VESSEL",
            "WORK VESSEL",
            "PLATFORM",
            "MISSION SHIP",
            "BUOY-LAYING VESSEL",
            "WELL STIMULATION VESSEL",
            "MOTOR HOPPER",
            "CABLE LAYER",
            "ANCHOR HANDLING/FIRE FIGHTING",
            "CRANE SHIP",
            "INLAND SUPPLY VESSEL",
            "OFFSHORE SUPPLY SHIP",
            "TRENCHING SUPPORT VESSEL",
            "OFFSHORE CONSTRUCTION JACK UP",
            "PILE DRIVING VESSEL",
            "REPLENISHMENT VESSEL",
            "CONSTRUCTION SUPPORT VESSEL",
            "PIPELAY CRANE VESSEL",
            "CRANE BARGE",
            "WORK PONTOON",
            "PRODUCTION TESTING VESSEL",
            "FLOATING SHEERLEG",
            "MOORING VESSEL",
            "DIVING SUPPORT PLATFORM",
            "SUPPORT JACK UP",
            "SEALER",
            "TRANS SHIPMENT VESSEL",
            "FLOATING LINKSPAN",
            "CRANE JACK UP",
            "PUMPING PLATFORM",
            "AIR CUSHION VESSEL",
            "POWER STATION VESSEL",
            "SUPPLY JACK UP",
            "RADAR PLATFORM",
            "JACKET LAUNCHING PONTOON",
            "PIPE LAYER PLATFORM",
            "PIPE BURYING VESSEL",
            "AIR CUSHION PATROL VESSEL",
            "AIR CUSHION WORK VESSEL",
            "PEARL SHELLS CARRIER",
            "STEAM SUPPLY PONTOON",
            "INCINERATOR",
            "JACK UP BARGE",
            "DESALINATION PONTOON",
            "GRAIN ELEVATING PONTOON",
            "DIVE VESSEL",
        ],
    },
    "SAILING VESSEL": {"SAILING VESSEL": ["SAILING VESSEL"]},
    "PLEASURE CRAFT": {
        "PLEASURE CRAFT": [
            "PLEASURE CRAFT",
            "YACHT",
            "MUSEUM SHIP",
            "EXHIBITION SHIP",
            "FLOATING HOTEL/RESTAURANT",
            "THEATRE VESSEL",
            "INLAND, PLEASURE CRAFT, >20 METRES",
        ]
    },
    "HIGH-SPEED CRAFT": {
        "HIGH-SPEED CRAFT": [
            "HIGH SPEED CRAFT",
            "HIGH-SPEED CRAFT",
            "HYDROFOIL",
            "HOVERCRAFT",
            "NAVAL CRAFT",
        ]
    },
    "SEARCH AND RESCUE": {
        "SAR": [
            "SAR",
            "SALVAGE/RESCUE VESSEL",
            "OFFSHORE SAFETY VESSEL",
            "STANDBY SAFETY VESSEL",
        ]
    },
    "PASSENGER": {
        "PASSENGER": [
            "PASSENGER",
            "PASSENGER SHIP",
            "PASSENGERS SHIP",
            "INLAND PASSENGERS SHIP",
            "INLAND FERRY",
            "FLOATING HOTEL",
            "FERRY",
            "RO-RO/PASSENGER SHIP",
            "ACCOMMODATION SHIP",
            "ACCOMMODATION BARGE",
            "ACCOMMODATION JACK UP",
            "ACCOMMODATION VESSEL",
            "PASSENGERS LANDING CRAFT",
            "HOUSEBOAT",
            "ACCOMMODATION PLATFORM",
            "AIR CUSHION PASSENGER SHIP",
            "AIR CUSHION RO-RO/PASSENGER SH",
            "INLAND, PASSENGER SHIP WITHOUT ACCOMMODATION",
        ]
    },
    "CARGO": {
        "CARGO": [
            "CARGO",
            "PASSENGER/CARGO SHIP",
            "LIVESTOCK CARRIER",
            "BULK CARRIER",
            "ORE CARRIER",
            "GENERAL CARGO",
            "WOOD CHIPS CARRIER",
            "CONTAINER SHIP",
            "RO-RO CARGO",
            "REEFER",
            "HEAVY LOAD CARRIER",
            "BARGE",
            "RO-RO/CONTAINER CARRIER",
            "INLAND CARGO",
            "CEMENT CARRIER",
            "REEFER/CONTAINERSHIP",
            "VEGETABLE/ANIMAL OIL TANKER",
            "OBO CARRIER",
            "VEHICLES CARRIER",
            "INLAND RO-RO CARGO SHIP",
            "RAIL/VEHICLES CARRIER",
            "PALLET CARRIER",
            "CARGO BARGE",
            "HOPPER BARGE",
            "DECK CARGO SHIP",
            "CARGO/CONTAINERSHIP",
            "AGGREGATES CARRIER",
            "LIMESTONE CARRIER",
            "ORE/OIL CARRIER",
            "SELF DISCHARGING BULK CARRIER",
            "DECK CARGO PONTOON",
            "BULK CARRIER WITH VEHICLE DECK",
            "PIPE CARRIER",
            "CEMENT BARGE",
            "STONE CARRIER",
            "BULK STORAGE BARGE",
            "AGGREGATES BARGE",
            "TIMBER CARRIER",
            "BULKER",
            "TRANS SHIPMENT BARGE",
            "POWDER CARRIER",
            "CABU CARRIER",
            "VEHICLE CARRIER",
        ],
        "CARGO - HAZARD A (MAJOR)": ["CARGO - HAZARD A (MAJOR)"],
        "CARGO - HAZARD B": ["CARGO - HAZARD B"],
        "CARGO - HAZARD C (MINOR)": ["CARGO - HAZARD C (MINOR)"],
        "CARGO - HAZARD D (RECOGNIZABLE)": ["CARGO - HAZARD D (RECOGNIZABLE)"],
    },
    "TANKER": {
        "TANKER": [
            "TANKER",
            "ASPHALT/BITUMEN TANKER",
            "CHEMICAL TANKER",
            "CRUDE OIL TANKER",
            "INLAND TANKER",
            "FRUIT JUICE TANKER",
            "BUNKERING TANKER",
            "WINE TANKER",
            "OIL PRODUCTS TANKER",
            "OIL/CHEMICAL TANKER",
            "WATER TANKER",
            "TANK BARGE",
            "EDIBLE OIL TANKER",
            "LPG/CHEMICAL TANKER",
            "SHUTTLE TANKER",
            "CO2 TANKER",
        ],
        "TANKER - HAZARD A (MAJOR)": ["TANKER - HAZARD A (MAJOR)"],
        "TANKER - HAZARD B": ["TANKER - HAZARD B"],
        "TANKER - HAZARD C (MINOR)": ["TANKER - HAZARD C (MINOR)"],
        "TANKER - HAZARD D (RECOGNIZABLE)": [
            "TANKER - HAZARD D (RECOGNIZABLE)",
            "LNG TANKER",
            "LPG TANKER",
            "GAS CARRIER",
        ],
    },
    "OTHER": {"OTHER": ["OTHER", "INLAND, SERVICE VESSEL, POLICE PATROL"]},
}
