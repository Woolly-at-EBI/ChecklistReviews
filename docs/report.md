# Review of the MIX-S checklists proposed by GSC
## Table of Contents


1 Review of the MIX-S checklists proposed by GSC  
2 Summary of Matches  
3 Exact Matches  
4 mixs_v6Terms without exact matches  
5 Frequency  
6 Harmonised Matches  
           



## Summary of Matches <a name="ReviewoftheMIX-SchecklistsproposedbyGSC"></a>
|                          | left_source   | right_source   |   left_count |   left_total |   right_count |   right_total |   cumulative_left | comment   |
|:-------------------------|:--------------|:---------------|-------------:|-------------:|--------------:|--------------:|------------------:|:----------|
| exact                    | ena_cl        | mixs_v6        |          367 |          625 |           367 |           795 |               367 |           |
| high_confident_matched   | ena_cl        | mixs_v6        |            8 |          625 |             8 |           795 |               375 |           |
| medium_confident_matched | ena_cl        | mixs_v6        |            6 |          625 |             6 |           795 |               381 |           |
| low_confident_matched    | ena_cl        | mixs_v6        |           20 |          625 |            14 |           795 |               401 |           |
| vlow_confident_matched   | ena_cl        | mixs_v6        |          186 |          625 |            96 |           795 |               587 |           |
| not_matched              | ena_cl        | mixs_v6        |           38 |          625 |           424 |           795 |               625 |           |
left sum: 625 out of 625  

Maximal total of mappings(changes to make) without adding new terms to ENA: 258  out of 625
right sum: 915 out of 795 terms are being captured, expecting a higher than total score as often an many to 1 match of terms in MIXS match

Maximal total of mappings(changes to make) without adding new terms to ENA: 428  out of 795


## Different types of Non-exact matches
 <BR>

### High confidence matches
<BR> This is mainly simple format differences, a no brainer to change?
 <BR>ENA count=8
 <BR>ENA: ['Depth', 'Salinity', 'Sample Collection Device', 'Size Fraction Lower Threshold', 'Size Fraction Upper Threshold', 'Temperature', 'host family relationship', 'surface air contaminant']
 <BR>MIXS: ['depth', 'salinity', 'sample collection device', 'size-fraction lower threshold', 'size-fraction upper threshold', 'temperature', 'host_family_relationship', 'surface-air contaminant']
 <BR>

### Medium confidence matches
 These are probably minor differences, a no brainer to change?
 <BR>ENA count=6
 <BR>ENA: ['biotic relationship', 'lung/nose-throat disorder', 'salinity method', 'sample transportation temperature', 'soil horizon method', 'total nitrogen method']
 <BR>MIXS: ['observed biotic relationship', 'nose throat disorder', 'salinity_meth', 'sample transport temperature', 'horizon method', 'total nitrogen content method']
 <BR>

### Low confidence matches
 These are higher risk, will need checking to change
 <BR>ENA count= 20
 <BR>ENA: ['16S recovery software', 'UViG assembly quality', 'air temperature', 'experimental factor 1', 'experimental factor 2', 'experimental factor 3', 'experimental factor 4', 'experimental factor 5', 'geographic location (country and/or sea)', 'geographic location (latitude)', 'geographic location (longitude)', 'host habitat', 'mean annual and seasonal precipitation', 'mean annual and seasonal temperature', 'sample collection device or method', 'sample storage conditions', 'sample weight for DNA extraction', 'soil water content', 'subspecific genetic lineage name', 'subspecific genetic lineage rank']
 <BR>MIXS: ['x_16s_recover_software', 'assembly quality', 'temperature', 'experimental factor', 'experimental factor', 'experimental factor', 'experimental factor', 'experimental factor', 'geographic location (country and/or sea,region)', 'geographic location (latitude and longitude)', 'geographic location (latitude and longitude)', 'host body habitat', 'mean seasonal precipitation', 'mean seasonal temperature', 'sample collection device', 'storage conditions', 'sample volume or weight for DNA extraction', 'water content', 'subspecific genetic lineage', 'subspecific genetic lineage']
 <BR>

## Exact Matches of ENA <a name="ExactMatches"></a>
douche, conductivity, fertilizer regimen, redox potential, gastrointestinal tract disorder, WGA amplification kit, ancestral data, wind speed, host total mass, pooling of DNA extracts (if done), sample capture status, sewage type, soluble reactive phosphorus, salinity, library vector, silicate, potassium, predicted genome type, growth facility, solar irradiance, organism count, tissue culture growth media, total phosphorus, geographic location (latitude and longitude), suspended particulate matter, slope gradient, adapters, feature prediction, altitude, binning parameters, rooting conditions, history/previous land use method, project name, pH method, host disease status, dissolved inorganic nitrogen, ethnicity, biotic regimen, growth hormone regimen, OTU classification approach, history/crop rotation, soil_taxonomic/FAO classification, bacterial respiration, chimera check software, host body product, host HIV status, seasonal environment, pregnancy, bishomohopanol, amniotic fluid/maternal health status, filter type, medical history performed, oxygenation status of sample, presence of pets or farm animals, sulfate, known pathogenicity, nitrogen, carbon dioxide, MAG coverage software, water content, wind direction, heating and cooling system type, plant growth medium, n-alkanes, host sex, microbial biomass, temperature, extreme_unusual_properties/heavy metals, plant structure, sludge retention time, total depth of water column, calcium, host last meal, history/fire, time since last toothbrushing, host phenotype, smoker, sequencing method, hysterectomy, links to additional analysis, host body habitat, dew point, host dry mass, host blood pressure systolic, phosphate, amniotic fluid/foetal health status, amount or size of sample collected, chlorophyll, density, lung/pulmonary disorder, occupancy at sampling, soil type, liver disorder, nitrate, pollutants, pressure, soluble inorganic material, amniotic fluid/gestation state, history/tillage, mean friction velocity, reactor type, climate environment, host diet, extreme_unusual_properties/Al saturation method, target subfragment, glucosidase activity, urine/kidney disorder, organic matter, soil pH, pcr conditions, twin sibling presence, host color, sample storage location, mineral nutrient regimen, organic carbon, environmental medium, urogenital disorder, plant sex, sodium, extreme_unusual_properties/Al saturation, host shape, gynecological disorder, source material identifiers, sample storage duration, taxonomic identity marker, nucleic acid extraction, rooting medium regulators, host body temperature, bromide, weight loss in last three months, OTU database, chemical oxygen demand, gaseous environment, ploidy, chemical mutagen, HRT, phaeopigments, extrachromosomal elements, host prediction approach, tRNA extraction software, current vegetation method, light type, turbidity, total carbon, broad-scale environmental context, library reads sequenced, soluble organic material, relationship to oxygen, menarche, link to classification information, relevant electronic resources, urine/collection method, relative air humidity, water content method, dissolved hydrogen, absolute air humidity, sample material processing, nitrite, host taxid, water temperature regimen, dermatology disorder, host substrate, light regimen, surface material, slope aspect, fungicide regimen, host pulse, total organic carbon, rooting medium solidifier, host genotype, non-mineral nutrient regimen, chemical administration, history/flooding, completeness approach, current vegetation, sample volume or weight for DNA extraction, tertiary treatment, library size, assembly quality, host body-mass index, host prediction estimated accuracy, particulate organic carbon, petroleum hydrocarbon, rainfall regimen, humidity regimen, aminopeptidase activity, space typical state, herbicide regimen, light intensity, host growth conditions, sample disease stage, similarity search method, study completion status, carbon monoxide, emulsions, alkyl diethers, major diet change in last six months, mean peak friction velocity, WGA amplification approach, binning software, host age, host scientific name, contamination screening input, building setting, downward PAR, fluorescence, link to climate information, sequence quality check, collection date, soil type method, indoor space, total particulate carbon, photon flux, drainage classification, biochemical oxygen demand, organic particles, contamination screening parameters, oxygen, detection type, ventilation rate, dissolved inorganic phosphorus, drug usage, ammonium, assembly software, encoded traits, host subject id, surface moisture, secondary treatment, magnesium, water current, profile position, occupant density at sampling, carbon/nitrogen ratio, host wet mass, microbial biomass method, methane, atmospheric data, target gene, watering regimen, plant product, host blood pressure diastolic, predicted genome structure, host height, gaseous substances, reassembly post binning, sample collection method, history/extreme events, isolation and growth condition, culture rooting medium, history/previous land use, dissolved carbon dioxide, humidity, rooting medium carbon, dissolved organic nitrogen, air temperature regimen, extreme_unusual_properties/heavy metals method, viral identification software, local environmental context, depth, standing water regimen, indoor surface, particulate organic nitrogen, genetic modification, host life stage, positive control type, dissolved inorganic carbon, typical occupant density, relevant standard operating procedures, blood/blood disorder, multiplex identifiers, surface moisture pH, taxonomic classification, host common name, birth control, completeness software, perturbation, surface temperature, air particulate matter concentration, sample collection device, inorganic particles, barometric pressure, biological status, menopause, soil_taxonomic/local classification method, industrial effluent percent, rooting medium organic supplements, sample size sorting method, size fraction selected, substructure type, bacterial production, antibiotic regimen, sexual activity, rooting medium micronutrients, dominant hand, negative control type, travel outside the country in last six months, radiation regimen, soil_taxonomic/local classification, building occupancy type, elevation, growth habit, pH regimen, gravidity, source of UViGs, contamination score, biomass, reference database(s), reference for biomaterial, sulfide, dissolved oxygen, suspended solids, ventilation type, soil texture method, organic nitrogen, dissolved organic carbon, history/agrochemical additions, library screening strategy, OTU sequence comparison approach, observed biotic relationship, experimental factor, urine/urogenital tract disorder, IHMC medication code, current land use, bacterial carbon production, mechanical damage, diether lipids, soil horizon, phospholipid fatty acid, total phosphate, chloride, decontamination software, gravity, salt regimen, wastewater type, rooting medium macronutrients, total inorganic nitrogen, estimated size, number of replicons, completeness score, host subspecific genetic lineage, number of standard tRNAs extracted, host occupation, pcr primers, propagation, time since last wash, surface humidity, alkalinity, pesticide regimen, host body site, tidal stage, host length, primary treatment, volatile organic compounds, rooting medium pH, subspecific genetic lineage, virus enrichment approach, efficiency percent, pH, trophic level, special diet, amniotic fluid/color, sorting technology, nucleic acid amplification, sample storage temperature, total dissolved nitrogen, pre-treatment, primary production

## mixs_v6Terms without exact matches, these are the most frequent <a name="mixs_v6Termswithoutexactmatches"></a>


### Table of Frequency on unexact GSC MIXS terms<a name="Frequency"></a>
| term                                                                   |   frequency |
|:-----------------------------------------------------------------------|------------:|
| geographic location (country and/or sea,region)                        |         277 |
| sample name                                                            |         275 |
| miscellaneous parameter                                                |         264 |
| taxonomy ID of DNA sample                                              |         254 |
| samp_collec_device                                                     |         254 |
| samp_collec_method                                                     |         254 |
| library layout                                                         |         233 |
| assembly name                                                          |         211 |
| annotation                                                             |         211 |
| number of contigs                                                      |         208 |
| host specificity or range                                              |         123 |
| observed host symbionts                                                |         108 |
| host_family_relation                                                   |          72 |
| sequencing location                                                    |          60 |
| food shipping transportation method                                    |          60 |
| culture isolation date                                                 |          60 |
| samp_stor_temp                                                         |          60 |
| food shipping transportation vehicle                                   |          60 |
| enrichment protocol                                                    |          60 |
| sample pooling                                                         |          60 |
| lot number                                                             |          60 |
| library preparation kit                                                |          60 |
| total nitrogen concentration                                           |          60 |
| spike-in microbial strain                                              |          48 |
| Interagency Food Safety Analytics Collaboration (IFSAC) category       |          48 |
| food container or wrapping                                             |          48 |
| sequencing kit                                                         |          48 |
| food treatment process                                                 |          48 |
| food source                                                            |          48 |
| culture result organism                                                |          48 |
| purpose of sampling                                                    |          48 |
| food contact surface                                                   |          48 |
| repository name                                                        |          48 |
| culture target microbial analyte                                       |          48 |
| food product type                                                      |          48 |
| food quality date                                                      |          48 |
| timepoint                                                              |          48 |
| total nitrogen content                                                 |          48 |
| culture result                                                         |          48 |
| sample source material category                                        |          48 |
| food preservation process                                              |          48 |
| food production system characteristics                                 |          48 |
| intended consumer                                                      |          48 |
| samp_stor_dur                                                          |          48 |
| sample type                                                            |          48 |
| part of plant or animal                                                |          48 |
| food packing medium                                                    |          48 |
| single_cell_lysis_appr                                                 |          47 |
| x_16s_recover                                                          |          47 |
| x_16s_recover_software                                                 |          47 |
| single_cell_lysis_prot                                                 |          47 |
| food additive                                                          |          36 |
| total organic carbon method                                            |          36 |
| sample transport temperature                                           |          36 |
| spike-in with heavy metals                                             |          36 |
| collection site geographic feature                                     |          36 |
| technical sample replicate                                             |          36 |
| food ingredient                                                        |          36 |
| food packing medium integrity                                          |          36 |
| mean seasonal precipitation                                            |          36 |
| food distribution point geographic location                            |          36 |
| spike-in bacterial serovar or serotype                                 |          36 |
| food product origin geographic location                                |          36 |
| spike-in growth medium                                                 |          36 |
| porosity                                                               |          36 |
| serovar or serotype                                                    |          36 |
| food package capacity                                                  |          36 |
| study design                                                           |          36 |
| study incubation temperature                                           |          36 |
| season                                                                 |          36 |
| sample transport  container                                            |          36 |
| food traceability list category                                        |          36 |
| sample transport duration                                              |          36 |
| Hazard Analysis Critical Control Points (HACCP) guide food safety term |          36 |
| study incubation duration                                              |          36 |
| mean seasonal temperature                                              |          36 |
| samp_stor_loc                                                          |          36 |
| sample storage media                                                   |          36 |
| biological sample replicate                                            |          36 |
| study treatment                                                        |          36 |
| food cooking process                                                   |          36 |
| spike in organism                                                      |          36 |
| bacteria density                                                       |          36 |
| material of contact prior to food packaging                            |          36 |
| spike-in with antibiotics                                              |          36 |
| sample storage device                                                  |          36 |
| microbiological culture medium                                         |          36 |
| alkalinity method                                                      |          36 |
| spike-in organism count                                                |          36 |
| food product by quality                                                |          36 |
| food product synonym                                                   |          36 |
| time-course duration                                                   |          36 |
| water source shared                                                    |          24 |
| relative location of sample                                            |          24 |
| horizon method                                                         |          24 |
| mean annual temperature                                                |          24 |
| fertilizer administration                                              |          24 |
| sulfate in formation water                                             |          24 |
| vfa in formation water                                                 |          24 |
| basin name                                                             |          24 |
| animal housing system                                                  |          24 |
| food distribution point geographic location (city)                     |          24 |
| viscosity                                                              |          24 |
| food animal source diet                                                |          24 |
| mean annual precipitation                                              |          24 |
| dissolved iron                                                         |          24 |
| sample subtype                                                         |          24 |
| field name                                                             |          24 |
| food product name legal status                                         |          24 |
| volatile fatty acids                                                   |          24 |
| crop yield                                                             |          24 |
| equipment shared with other farms                                      |          24 |
| sample transport conditions                                            |          24 |
| number of samples collected                                            |          24 |
| total iron                                                             |          24 |
| farm equipment sanitization                                            |          24 |
| food allergen labeling                                                 |          24 |
| ethylbenzene                                                           |          24 |
| xylene                                                                 |          24 |
| dissolved oxygen in fluids                                             |          24 |
| pour point                                                             |          24 |
| mean seasonal humidity                                                 |          24 |
| hydrocarbon resource geological age                                    |          24 |
| additional info                                                        |          24 |
| benzene                                                                |          24 |
| food production characteristics                                        |          24 |
| sample well name                                                       |          24 |
| formation water salinity                                               |          24 |
| Food harvesting process                                                |          24 |
| resins wt%                                                             |          24 |
| dietary claim or use                                                   |          24 |
| soil conductivity                                                      |          24 |
| sieving                                                                |          24 |
| hydrocarbon resource original pressure                                 |          24 |
| saturates wt%                                                          |          24 |
| nose throat disorder                                                   |          24 |
| aromatics wt%                                                          |          24 |
| food stored by consumer (storage duration)                             |          24 |
| reservoir name                                                         |          24 |
| food stored by consumer (storage temperature)                          |          24 |
| organism count qPCR information                                        |          24 |
| food animal group size                                                 |          24 |
| toluene                                                                |          24 |
| total nitrogen content method                                          |          24 |
| production labeling claims                                             |          24 |
| room dimensions                                                        |          24 |
| depth (TVDSS) of hydrocarbon resource pressure                         |          24 |
| sampling room ID or name                                               |          24 |
| purchase date                                                          |          24 |
| total acid number                                                      |          24 |
| salinity_meth                                                          |          24 |
| water pH                                                               |          24 |
| API gravity                                                            |          24 |
| environment adjacent to site                                           |          24 |
| farm watering water source                                             |          24 |
| frequency of cleaning                                                  |          24 |
| antimicrobial phenotype of spike-in bacteria                           |          24 |
| soil cover                                                             |          24 |
| hydrocarbon resource type                                              |          24 |
| depth (TVDSS) of hydrocarbon resource temperature                      |          24 |
| depositional environment                                               |          24 |
| samp_salinity                                                          |          24 |
| animal feeding equipment                                               |          24 |
| storage conditions                                                     |          24 |
| sampling floor                                                         |          24 |
| quantity purchased                                                     |          24 |
| total sulfur                                                           |          24 |
| nucleic acid extraction kit                                            |          24 |
| hydrocarbon resource original temperature                              |          24 |
| lithology                                                              |          24 |
| animal water delivery method                                           |          24 |
| well identification number                                             |          24 |
| farm equipment used                                                    |          24 |
| average daily occupancy                                                |          24 |
| asphaltenes wt%                                                        |          24 |
| hydrocarbon type produced                                              |          24 |
| plant water delivery method                                            |          24 |
| presence of pets, animals, or insects                                  |          24 |
| microbial starter                                                      |          12 |
| injection water fraction                                               |          12 |
| quadrant position                                                      |          12 |
| host of the symbiotic host disease status                              |          12 |
| furniture                                                              |          12 |
| architectural structure                                                |          12 |
| exterior door count                                                    |          12 |
| last time swept/mopped/vacuumed                                        |          12 |
| wall thermal mass                                                      |          12 |
| tot_n_meth                                                             |          12 |
| orientations of exterior wall                                          |          12 |
| wall surface treatment                                                 |          12 |
| facility type                                                          |          12 |
| fermentation chemical additives percentage                             |          12 |
| fermentation chemical additives                                        |          12 |
| biocide                                                                |          12 |
| type of symbiosis                                                      |          12 |
| relative sampling location                                             |          12 |
| food production environmental monitoring zone                          |          12 |
| wall height                                                            |          12 |
| secondary and tertiary recovery methods and start date                 |          12 |
| floor thermal mass                                                     |          12 |
| injection water breakthrough date of specific well                     |          12 |
| symbiotic host organism life cycle type                                |          12 |
| food cleaning process                                                  |          12 |
| mechanical structure                                                   |          12 |
| production start date                                                  |          12 |
| ceiling condition                                                      |          12 |
| escalator count                                                        |          12 |
| shading device material                                                |          12 |
| soil texture classification                                            |          12 |
| growth medium                                                          |          12 |
| tot_car                                                                |          12 |
| fermentation temperature                                               |          12 |
| chemical treatment                                                     |          12 |
| frequency of cooking                                                   |          12 |
| weekday                                                                |          12 |
| rooms that share a door with sampling room                             |          12 |
| host specificity                                                       |          12 |
| food animal antimicrobial route of administration                      |          12 |
| room window count                                                      |          12 |
| rooms connected by a doorway                                           |          12 |
| built structure setting                                                |          12 |
| room volume                                                            |          12 |
| floor finish material                                                  |          12 |
| Food_Product_type                                                      |          12 |
| cooling system identifier                                              |          12 |
| previous_land_use_meth                                                 |          12 |
| gender of restroom                                                     |          12 |
| fermentation headspace oxygen                                          |          12 |
| train stop collection location                                         |          12 |
| animal intrusion near sample source                                    |          12 |
| window horizontal position                                             |          12 |
| door type, composite                                                   |          12 |
| texture_meth                                                           |          12 |
| source rock lithology                                                  |          12 |
| oil water contact depth                                                |          12 |
| sampling room sterilization method                                     |          12 |
| visual media                                                           |          12 |
| door signs of water/mold                                               |          12 |
| door type, wood                                                        |          12 |
| host of the symbiotic host taxon id                                    |          12 |
| floor condition                                                        |          12 |
| ceiling type                                                           |          12 |
| room count                                                             |          12 |
| chemical treatment method                                              |          12 |
| shading device condition                                               |          12 |
| host of the symbiotic host infra-specific name                         |          12 |
| host_infra_specific_name                                               |          12 |
| average temperature                                                    |          12 |
| microbial starter organism count                                       |          12 |
| sample surface moisture                                                |          12 |
| permeability                                                           |          12 |
| specifications                                                         |          12 |
| window status                                                          |          12 |
| heating delivery locations                                             |          12 |
| wall area                                                              |          12 |
| heating system delivery method                                         |          12 |
| particle classification                                                |          12 |
| host of the symbiotic host family relationship                         |          12 |
| sample measured depth                                                  |          12 |
| food animal antimicrobial                                              |          12 |
| sample location condition                                              |          12 |
| host of the symbiotic host gravidity                                   |          12 |
| window area/size                                                       |          12 |
| water delivery frequency                                               |          12 |
| room architectural elements                                            |          12 |
| biocide administration                                                 |          12 |
| mode of transmission                                                   |          12 |
| extreme weather date                                                   |          12 |
| bedroom count                                                          |          12 |
| plant reproductive part                                                |          12 |
| heating system identifier                                              |          12 |
| microbial starter preparation                                          |          12 |
| photosynthetic activity                                                |          12 |
| date last rain                                                         |          12 |
| built structure type                                                   |          12 |
| host number individual                                                 |          12 |
| sediment type                                                          |          12 |
| local air flow impediments                                             |          12 |
| room sampling position                                                 |          12 |
| floor area                                                             |          12 |
| shading device location                                                |          12 |
| window location                                                        |          12 |
| water feature size                                                     |          12 |
| room net area                                                          |          12 |
| host of the symbiotic host subject id                                  |          12 |
| door condition                                                         |          12 |
| adjacent rooms                                                         |          12 |
| host of the symbiotic host local environmental context                 |          12 |
| fermentation vessel                                                    |          12 |
| aerospace structure                                                    |          12 |
| room condition                                                         |          12 |
| orientations of exterior window                                        |          12 |
| exposed ductwork                                                       |          12 |
| sample_collec_method                                                   |          12 |
| food animal body condition                                             |          12 |
| photosynthetic activity method                                         |          12 |
| host of the symbiotic host common name                                 |          12 |
| fermentation relative humidity                                         |          12 |
| floor count                                                            |          12 |
| wall location                                                          |          12 |
| window vertical position                                               |          12 |
| outside relative humidity                                              |          12 |
| sample collection point                                                |          12 |
| amount of light                                                        |          12 |
| inside lux light                                                       |          12 |
| number of pets                                                         |          12 |
| number of houseplants                                                  |          12 |
| water production rate                                                  |          12 |
| microbial starter NCBI taxonomy ID                                     |          12 |
| wall construction type                                                 |          12 |
| interior wall condition                                                |          12 |
| ceiling finish material                                                |          12 |
| height carpet fiber mat                                                |          12 |
| source rock geological age                                             |          12 |
| room door distance                                                     |          12 |
| sampling time outside                                                  |          12 |
| host of the symbiont role                                              |          12 |
| assembly_quality                                                       |          12 |
| area sampled size                                                      |          12 |
| window covering                                                        |          12 |
| food animal antimicrobial duration                                     |          12 |
| hygienic food production area                                          |          12 |
| room occupancy                                                         |          12 |
| handidness                                                             |          12 |
| room type                                                              |          12 |
| maximum occupancy                                                      |          12 |
| seasonal use                                                           |          12 |
| observed coinfecting organisms in host of host                         |          12 |
| door area or size                                                      |          12 |
| sample storage solution                                                |          12 |
| host_infra_specific_rank                                               |          12 |
| shading device type                                                    |          12 |
| air_particulate_matter_concentration                                   |          12 |
| food animal antimicrobial frequency                                    |          12 |
| host cellular location                                                 |          12 |
| microbial starter inoculation                                          |          12 |
| train line                                                             |          12 |
| url                                                                    |          12 |
| source rock depositional environment                                   |          12 |
| train station collection location                                      |          12 |
| door location                                                          |          12 |
| floor structure                                                        |          12 |
| sample true vertical depth subsea                                      |          12 |
| biocide administration method                                          |          12 |
| soil sediment porosity                                                 |          12 |
| door direction of opening                                              |          12 |
| fireplace type                                                         |          12 |
| sampling day weather                                                   |          12 |
| room location in building                                              |          12 |
| door type                                                              |          12 |
| microbial starter source                                               |          12 |
| production rate                                                        |          12 |
| rooms that share a wall with sampling room                             |          12 |
| window condition                                                       |          12 |
| duration of association with the host                                  |          12 |
| ceiling signs of water/mold                                            |          12 |
| door type, metal                                                       |          12 |
| farm equipment sanitization frequency                                  |          12 |
| soil_text_measure                                                      |          12 |
| number of residents                                                    |          12 |
| source rock kerogen type                                               |          12 |
| room air exchange rate                                                 |          12 |
| host of the symbiotic host total mass                                  |          12 |
| door movement                                                          |          12 |
| ceiling thermal mass                                                   |          12 |
| floor signs of water/mold                                              |          12 |
| hallway/corridor count                                                 |          12 |
| extreme weather event                                                  |          12 |
| water cut                                                              |          12 |
| shading device signs of water/mold                                     |          12 |
| fermentation time                                                      |          12 |
| rooms that are on the same hallway                                     |          12 |
| food source age                                                        |          12 |
| water feature type                                                     |          12 |
| sample_name                                                            |          12 |
| route of transmission                                                  |          12 |
| door material                                                          |          12 |
| host dependence                                                        |          12 |
| corrosion rate at sample location                                      |          12 |
| exposed pipes                                                          |          12 |
| degree of plant part maturity                                          |          12 |
| tot_phos                                                               |          12 |
| window open frequency                                                  |          12 |
| non_mineral_nutr_regm                                                  |          12 |
| environmental feature adjacent water source                            |          12 |
| host of the symbiotic host genotype                                    |          12 |
| design, construction, and operation documents                          |          12 |
| ceiling area                                                           |          12 |
| wall signs of water/mold                                               |          12 |
| address                                                                |          12 |
| built structure age                                                    |          12 |
| elevator count                                                         |          12 |
| bathroom count                                                         |          12 |
| Food_source                                                            |          12 |
| texture                                                                |          12 |
| window signs of water/mold                                             |          12 |
| host of the symbiotic host infra-specific rank                         |          12 |
| fermentation medium                                                    |          12 |
| window type                                                            |          12 |
| fertilizer administration date                                         |          12 |
| preservative added to sample                                           |          12 |
| specific intended consumer                                             |          12 |
| food animal source sex category                                        |          12 |
| host of the symbiotic host phenotype                                   |          12 |
| specific humidity                                                      |          12 |
| temperature outside house                                              |          12 |
| occupancy documentation                                                |          12 |
| wall finish material                                                   |          12 |
| host of the symbiotic host environemental medium                       |          12 |
| ceiling structure                                                      |          12 |
| ceiling texture                                                        |          12 |
| room moisture damage or mold history                                   |          12 |
| drawings                                                               |          12 |
| food animal antimicrobial intended use                                 |          12 |
| horizon                                                                |          12 |
| wall texture                                                           |          12 |
| microbial_biomass_meth                                                 |          12 |
| fermentation pH                                                        |          12 |
| average dew point                                                      |          12 |
| floor age                                                              |          12 |
| window material                                                        |          12 |
| has_numeric_value                                                      |           1 |
| has_unit                                                               |           1 |
| has_raw_value                                                          |           1 |


## Harmonised Matches <a name="HarmonisedMatches"></a>
| left_term                                       | match_type   | match                                           |   fuzzy_score | match_term_duplicated   |   likely_map_accuracy | map_accuracy_des                                          |
|:------------------------------------------------|:-------------|:------------------------------------------------|--------------:|:------------------------|----------------------:|:----------------------------------------------------------|
| 16S recovery software                           | fuzzy        | x_16s_recover_software                          |            93 | True                    |                   0.5 | left and right one word apart, but also matched elsewhere |
| Depth                                           | harmonised   | depth                                           |           100 | True                    |                   1   | very_close                                                |
| HRT                                             | exact        | HRT                                             |           100 | False                   |                   1   | exact                                                     |
| IHMC medication code                            | exact        | IHMC medication code                            |           100 | False                   |                   1   | exact                                                     |
| MAG coverage software                           | exact        | MAG coverage software                           |           100 | True                    |                   1   | exact                                                     |
| OTU classification approach                     | exact        | OTU classification approach                     |           100 | True                    |                   1   | exact                                                     |
| OTU database                                    | exact        | OTU database                                    |           100 | False                   |                   1   | exact                                                     |
| OTU sequence comparison approach                | exact        | OTU sequence comparison approach                |           100 | False                   |                   1   | exact                                                     |
| Salinity                                        | harmonised   | salinity                                        |           100 | True                    |                   1   | very_close                                                |
| Sample Collection Device                        | harmonised   | sample collection device                        |           100 | True                    |                   1   | very_close                                                |
| Size Fraction Lower Threshold                   | harmonised   | size-fraction lower threshold                   |           100 | False                   |                   1   | very_close                                                |
| Size Fraction Upper Threshold                   | harmonised   | size-fraction upper threshold                   |           100 | False                   |                   1   | very_close                                                |
| Temperature                                     | harmonised   | temperature                                     |           100 | True                    |                   1   | very_close                                                |
| UViG assembly quality                           | fuzzy        | assembly quality                                |            95 | True                    |                   0.3 | right is a substring of left, but also matched elsewhere  |
| WGA amplification approach                      | exact        | WGA amplification approach                      |           100 | False                   |                   1   | exact                                                     |
| WGA amplification kit                           | exact        | WGA amplification kit                           |           100 | True                    |                   1   | exact                                                     |
| absolute air humidity                           | exact        | absolute air humidity                           |           100 | False                   |                   1   | exact                                                     |
| adapters                                        | exact        | adapters                                        |           100 | False                   |                   1   | exact                                                     |
| air particulate matter concentration            | exact        | air particulate matter concentration            |           100 | True                    |                   1   | exact                                                     |
| air temperature                                 | fuzzy        | temperature                                     |            95 | True                    |                   0.3 | right is a substring of left, but also matched elsewhere  |
| air temperature regimen                         | exact        | air temperature regimen                         |           100 | False                   |                   1   | exact                                                     |
| alkalinity                                      | exact        | alkalinity                                      |           100 | False                   |                   1   | exact                                                     |
| alkyl diethers                                  | exact        | alkyl diethers                                  |           100 | False                   |                   1   | exact                                                     |
| altitude                                        | exact        | altitude                                        |           100 | False                   |                   1   | exact                                                     |
| aminopeptidase activity                         | exact        | aminopeptidase activity                         |           100 | False                   |                   1   | exact                                                     |
| ammonium                                        | exact        | ammonium                                        |           100 | False                   |                   1   | exact                                                     |
| amniotic fluid/color                            | exact        | amniotic fluid/color                            |           100 | False                   |                   1   | exact                                                     |
| amniotic fluid/foetal health status             | exact        | amniotic fluid/foetal health status             |           100 | True                    |                   1   | exact                                                     |
| amniotic fluid/gestation state                  | exact        | amniotic fluid/gestation state                  |           100 | False                   |                   1   | exact                                                     |
| amniotic fluid/maternal health status           | exact        | amniotic fluid/maternal health status           |           100 | False                   |                   1   | exact                                                     |
| amount or size of sample collected              | exact        | amount or size of sample collected              |           100 | True                    |                   1   | exact                                                     |
| ancestral data                                  | exact        | ancestral data                                  |           100 | False                   |                   1   | exact                                                     |
| antibiotic regimen                              | exact        | antibiotic regimen                              |           100 | False                   |                   1   | exact                                                     |
| assembly quality                                | exact        | assembly quality                                |           100 | True                    |                   1   | exact                                                     |
| assembly software                               | exact        | assembly software                               |           100 | False                   |                   1   | exact                                                     |
| atmospheric data                                | exact        | atmospheric data                                |           100 | False                   |                   1   | exact                                                     |
| bacterial carbon production                     | exact        | bacterial carbon production                     |           100 | False                   |                   1   | exact                                                     |
| bacterial production                            | exact        | bacterial production                            |           100 | False                   |                   1   | exact                                                     |
| bacterial respiration                           | exact        | bacterial respiration                           |           100 | False                   |                   1   | exact                                                     |
| barometric pressure                             | exact        | barometric pressure                             |           100 | False                   |                   1   | exact                                                     |
| binning parameters                              | exact        | binning parameters                              |           100 | False                   |                   1   | exact                                                     |
| binning software                                | exact        | binning software                                |           100 | False                   |                   1   | exact                                                     |
| biochemical oxygen demand                       | exact        | biochemical oxygen demand                       |           100 | False                   |                   1   | exact                                                     |
| biological status                               | exact        | biological status                               |           100 | False                   |                   1   | exact                                                     |
| biomass                                         | exact        | biomass                                         |           100 | False                   |                   1   | exact                                                     |
| biotic regimen                                  | exact        | biotic regimen                                  |           100 | False                   |                   1   | exact                                                     |
| biotic relationship                             | fuzzy        | observed biotic relationship                    |            95 | True                    |                   0.7 | left is a substring of right, but also matched elsewhere  |
| birth control                                   | exact        | birth control                                   |           100 | False                   |                   1   | exact                                                     |
| bishomohopanol                                  | exact        | bishomohopanol                                  |           100 | False                   |                   1   | exact                                                     |
| blood/blood disorder                            | exact        | blood/blood disorder                            |           100 | True                    |                   1   | exact                                                     |
| broad-scale environmental context               | exact        | broad-scale environmental context               |           100 | True                    |                   1   | exact                                                     |
| bromide                                         | exact        | bromide                                         |           100 | False                   |                   1   | exact                                                     |
| building occupancy type                         | exact        | building occupancy type                         |           100 | True                    |                   1   | exact                                                     |
| building setting                                | exact        | building setting                                |           100 | False                   |                   1   | exact                                                     |
| calcium                                         | exact        | calcium                                         |           100 | False                   |                   1   | exact                                                     |
| carbon dioxide                                  | exact        | carbon dioxide                                  |           100 | False                   |                   1   | exact                                                     |
| carbon monoxide                                 | exact        | carbon monoxide                                 |           100 | False                   |                   1   | exact                                                     |
| carbon/nitrogen ratio                           | exact        | carbon/nitrogen ratio                           |           100 | False                   |                   1   | exact                                                     |
| chemical administration                         | exact        | chemical administration                         |           100 | False                   |                   1   | exact                                                     |
| chemical mutagen                                | exact        | chemical mutagen                                |           100 | False                   |                   1   | exact                                                     |
| chemical oxygen demand                          | exact        | chemical oxygen demand                          |           100 | False                   |                   1   | exact                                                     |
| chimera check software                          | exact        | chimera check software                          |           100 | False                   |                   1   | exact                                                     |
| chloride                                        | exact        | chloride                                        |           100 | False                   |                   1   | exact                                                     |
| chlorophyll                                     | exact        | chlorophyll                                     |           100 | True                    |                   1   | exact                                                     |
| climate environment                             | exact        | climate environment                             |           100 | False                   |                   1   | exact                                                     |
| collection date                                 | exact        | collection date                                 |           100 | True                    |                   1   | exact                                                     |
| completeness approach                           | exact        | completeness approach                           |           100 | False                   |                   1   | exact                                                     |
| completeness score                              | exact        | completeness score                              |           100 | False                   |                   1   | exact                                                     |
| completeness software                           | exact        | completeness software                           |           100 | False                   |                   1   | exact                                                     |
| conductivity                                    | exact        | conductivity                                    |           100 | False                   |                   1   | exact                                                     |
| contamination score                             | exact        | contamination score                             |           100 | False                   |                   1   | exact                                                     |
| contamination screening input                   | exact        | contamination screening input                   |           100 | False                   |                   1   | exact                                                     |
| contamination screening parameters              | exact        | contamination screening parameters              |           100 | False                   |                   1   | exact                                                     |
| culture rooting medium                          | exact        | culture rooting medium                          |           100 | False                   |                   1   | exact                                                     |
| current land use                                | exact        | current land use                                |           100 | False                   |                   1   | exact                                                     |
| current vegetation                              | exact        | current vegetation                              |           100 | False                   |                   1   | exact                                                     |
| current vegetation method                       | exact        | current vegetation method                       |           100 | False                   |                   1   | exact                                                     |
| decontamination software                        | exact        | decontamination software                        |           100 | True                    |                   1   | exact                                                     |
| density                                         | exact        | density                                         |           100 | False                   |                   1   | exact                                                     |
| depth                                           | exact        | depth                                           |           100 | True                    |                   1   | exact                                                     |
| dermatology disorder                            | exact        | dermatology disorder                            |           100 | False                   |                   1   | exact                                                     |
| detection type                                  | exact        | detection type                                  |           100 | False                   |                   1   | exact                                                     |
| dew point                                       | exact        | dew point                                       |           100 | True                    |                   1   | exact                                                     |
| diether lipids                                  | exact        | diether lipids                                  |           100 | False                   |                   1   | exact                                                     |
| dissolved carbon dioxide                        | exact        | dissolved carbon dioxide                        |           100 | False                   |                   1   | exact                                                     |
| dissolved hydrogen                              | exact        | dissolved hydrogen                              |           100 | False                   |                   1   | exact                                                     |
| dissolved inorganic carbon                      | exact        | dissolved inorganic carbon                      |           100 | False                   |                   1   | exact                                                     |
| dissolved inorganic nitrogen                    | exact        | dissolved inorganic nitrogen                    |           100 | False                   |                   1   | exact                                                     |
| dissolved inorganic phosphorus                  | exact        | dissolved inorganic phosphorus                  |           100 | False                   |                   1   | exact                                                     |
| dissolved organic carbon                        | exact        | dissolved organic carbon                        |           100 | False                   |                   1   | exact                                                     |
| dissolved organic nitrogen                      | exact        | dissolved organic nitrogen                      |           100 | False                   |                   1   | exact                                                     |
| dissolved oxygen                                | exact        | dissolved oxygen                                |           100 | False                   |                   1   | exact                                                     |
| dominant hand                                   | exact        | dominant hand                                   |           100 | False                   |                   1   | exact                                                     |
| douche                                          | exact        | douche                                          |           100 | False                   |                   1   | exact                                                     |
| downward PAR                                    | exact        | downward PAR                                    |           100 | False                   |                   1   | exact                                                     |
| drainage classification                         | exact        | drainage classification                         |           100 | False                   |                   1   | exact                                                     |
| drug usage                                      | exact        | drug usage                                      |           100 | False                   |                   1   | exact                                                     |
| efficiency percent                              | exact        | efficiency percent                              |           100 | False                   |                   1   | exact                                                     |
| elevation                                       | exact        | elevation                                       |           100 | False                   |                   1   | exact                                                     |
| emulsions                                       | exact        | emulsions                                       |           100 | False                   |                   1   | exact                                                     |
| encoded traits                                  | exact        | encoded traits                                  |           100 | False                   |                   1   | exact                                                     |
| environmental medium                            | exact        | environmental medium                            |           100 | False                   |                   1   | exact                                                     |
| estimated size                                  | exact        | estimated size                                  |           100 | False                   |                   1   | exact                                                     |
| ethnicity                                       | exact        | ethnicity                                       |           100 | False                   |                   1   | exact                                                     |
| experimental factor                             | exact        | experimental factor                             |           100 | True                    |                   1   | exact                                                     |
| experimental factor 1                           | fuzzy        | experimental factor                             |            95 | True                    |                   0.5 | left has numerical suffix                                 |
| experimental factor 2                           | fuzzy        | experimental factor                             |            95 | True                    |                   0.5 | left has numerical suffix                                 |
| experimental factor 3                           | fuzzy        | experimental factor                             |            95 | True                    |                   0.5 | left has numerical suffix                                 |
| experimental factor 4                           | fuzzy        | experimental factor                             |            95 | True                    |                   0.5 | left has numerical suffix                                 |
| experimental factor 5                           | fuzzy        | experimental factor                             |            95 | True                    |                   0.5 | left has numerical suffix                                 |
| extrachromosomal elements                       | exact        | extrachromosomal elements                       |           100 | False                   |                   1   | exact                                                     |
| extreme_unusual_properties/Al saturation        | exact        | extreme_unusual_properties/Al saturation        |           100 | False                   |                   1   | exact                                                     |
| extreme_unusual_properties/Al saturation method | exact        | extreme_unusual_properties/Al saturation method |           100 | True                    |                   1   | exact                                                     |
| extreme_unusual_properties/heavy metals         | exact        | extreme_unusual_properties/heavy metals         |           100 | False                   |                   1   | exact                                                     |
| extreme_unusual_properties/heavy metals method  | exact        | extreme_unusual_properties/heavy metals method  |           100 | False                   |                   1   | exact                                                     |
| feature prediction                              | exact        | feature prediction                              |           100 | False                   |                   1   | exact                                                     |
| fertilizer regimen                              | exact        | fertilizer regimen                              |           100 | False                   |                   1   | exact                                                     |
| filter type                                     | exact        | filter type                                     |           100 | True                    |                   1   | exact                                                     |
| fluorescence                                    | exact        | fluorescence                                    |           100 | False                   |                   1   | exact                                                     |
| fungicide regimen                               | exact        | fungicide regimen                               |           100 | False                   |                   1   | exact                                                     |
| gaseous environment                             | exact        | gaseous environment                             |           100 | False                   |                   1   | exact                                                     |
| gaseous substances                              | exact        | gaseous substances                              |           100 | False                   |                   1   | exact                                                     |
| gastrointestinal tract disorder                 | exact        | gastrointestinal tract disorder                 |           100 | False                   |                   1   | exact                                                     |
| genetic modification                            | exact        | genetic modification                            |           100 | False                   |                   1   | exact                                                     |
| geographic location (country and/or sea)        | fuzzy        | geographic location (country and/or sea,region) |            95 | True                    |                   0.5 | left and right one word apart, but also matched elsewhere |
| geographic location (latitude and longitude)    | exact        | geographic location (latitude and longitude)    |           100 | True                    |                   1   | exact                                                     |
| geographic location (latitude)                  | fuzzy        | geographic location (latitude and longitude)    |            95 | True                    |                   0.5 | left and right one word apart, but also matched elsewhere |
| geographic location (longitude)                 | fuzzy        | geographic location (latitude and longitude)    |            95 | True                    |                   0.5 | left and right one word apart, but also matched elsewhere |
| glucosidase activity                            | exact        | glucosidase activity                            |           100 | False                   |                   1   | exact                                                     |
| gravidity                                       | exact        | gravidity                                       |           100 | False                   |                   1   | exact                                                     |
| gravity                                         | exact        | gravity                                         |           100 | False                   |                   1   | exact                                                     |
| growth facility                                 | exact        | growth facility                                 |           100 | False                   |                   1   | exact                                                     |
| growth habit                                    | exact        | growth habit                                    |           100 | False                   |                   1   | exact                                                     |
| growth hormone regimen                          | exact        | growth hormone regimen                          |           100 | False                   |                   1   | exact                                                     |
| gynecological disorder                          | exact        | gynecological disorder                          |           100 | False                   |                   1   | exact                                                     |
| heating and cooling system type                 | exact        | heating and cooling system type                 |           100 | False                   |                   1   | exact                                                     |
| herbicide regimen                               | exact        | herbicide regimen                               |           100 | False                   |                   1   | exact                                                     |
| history/agrochemical additions                  | exact        | history/agrochemical additions                  |           100 | True                    |                   1   | exact                                                     |
| history/crop rotation                           | exact        | history/crop rotation                           |           100 | False                   |                   1   | exact                                                     |
| history/extreme events                          | exact        | history/extreme events                          |           100 | False                   |                   1   | exact                                                     |
| history/fire                                    | exact        | history/fire                                    |           100 | False                   |                   1   | exact                                                     |
| history/flooding                                | exact        | history/flooding                                |           100 | False                   |                   1   | exact                                                     |
| history/previous land use                       | exact        | history/previous land use                       |           100 | False                   |                   1   | exact                                                     |
| history/previous land use method                | exact        | history/previous land use method                |           100 | False                   |                   1   | exact                                                     |
| history/tillage                                 | exact        | history/tillage                                 |           100 | False                   |                   1   | exact                                                     |
| host HIV status                                 | exact        | host HIV status                                 |           100 | False                   |                   1   | exact                                                     |
| host age                                        | exact        | host age                                        |           100 | False                   |                   1   | exact                                                     |
| host blood pressure diastolic                   | exact        | host blood pressure diastolic                   |           100 | False                   |                   1   | exact                                                     |
| host blood pressure systolic                    | exact        | host blood pressure systolic                    |           100 | False                   |                   1   | exact                                                     |
| host body habitat                               | exact        | host body habitat                               |           100 | True                    |                   1   | exact                                                     |
| host body product                               | exact        | host body product                               |           100 | False                   |                   1   | exact                                                     |
| host body site                                  | exact        | host body site                                  |           100 | True                    |                   1   | exact                                                     |
| host body temperature                           | exact        | host body temperature                           |           100 | False                   |                   1   | exact                                                     |
| host body-mass index                            | exact        | host body-mass index                            |           100 | False                   |                   1   | exact                                                     |
| host color                                      | exact        | host color                                      |           100 | False                   |                   1   | exact                                                     |
| host common name                                | exact        | host common name                                |           100 | False                   |                   1   | exact                                                     |
| host diet                                       | exact        | host diet                                       |           100 | True                    |                   1   | exact                                                     |
| host disease status                             | exact        | host disease status                             |           100 | True                    |                   1   | exact                                                     |
| host dry mass                                   | exact        | host dry mass                                   |           100 | False                   |                   1   | exact                                                     |
| host family relationship                        | harmonised   | host_family_relationship                        |           100 | False                   |                   1   | very_close                                                |
| host genotype                                   | exact        | host genotype                                   |           100 | True                    |                   1   | exact                                                     |
| host growth conditions                          | exact        | host growth conditions                          |           100 | False                   |                   1   | exact                                                     |
| host habitat                                    | fuzzy        | host body habitat                               |            95 | True                    |                   0.5 | left and right one word apart, but also matched elsewhere |
| host height                                     | exact        | host height                                     |           100 | False                   |                   1   | exact                                                     |
| host last meal                                  | exact        | host last meal                                  |           100 | False                   |                   1   | exact                                                     |
| host length                                     | exact        | host length                                     |           100 | False                   |                   1   | exact                                                     |
| host life stage                                 | exact        | host life stage                                 |           100 | True                    |                   1   | exact                                                     |
| host occupation                                 | exact        | host occupation                                 |           100 | False                   |                   1   | exact                                                     |
| host phenotype                                  | exact        | host phenotype                                  |           100 | False                   |                   1   | exact                                                     |
| host prediction approach                        | exact        | host prediction approach                        |           100 | False                   |                   1   | exact                                                     |
| host prediction estimated accuracy              | exact        | host prediction estimated accuracy              |           100 | False                   |                   1   | exact                                                     |
| host pulse                                      | exact        | host pulse                                      |           100 | False                   |                   1   | exact                                                     |
| host scientific name                            | exact        | host scientific name                            |           100 | False                   |                   1   | exact                                                     |
| host sex                                        | exact        | host sex                                        |           100 | True                    |                   1   | exact                                                     |
| host shape                                      | exact        | host shape                                      |           100 | False                   |                   1   | exact                                                     |
| host subject id                                 | exact        | host subject id                                 |           100 | False                   |                   1   | exact                                                     |
| host subspecific genetic lineage                | exact        | host subspecific genetic lineage                |           100 | False                   |                   1   | exact                                                     |
| host substrate                                  | exact        | host substrate                                  |           100 | False                   |                   1   | exact                                                     |
| host taxid                                      | exact        | host taxid                                      |           100 | False                   |                   1   | exact                                                     |
| host total mass                                 | exact        | host total mass                                 |           100 | False                   |                   1   | exact                                                     |
| host wet mass                                   | exact        | host wet mass                                   |           100 | False                   |                   1   | exact                                                     |
| humidity                                        | exact        | humidity                                        |           100 | False                   |                   1   | exact                                                     |
| humidity regimen                                | exact        | humidity regimen                                |           100 | False                   |                   1   | exact                                                     |
| hysterectomy                                    | exact        | hysterectomy                                    |           100 | False                   |                   1   | exact                                                     |
| indoor space                                    | exact        | indoor space                                    |           100 | False                   |                   1   | exact                                                     |
| indoor surface                                  | exact        | indoor surface                                  |           100 | False                   |                   1   | exact                                                     |
| industrial effluent percent                     | exact        | industrial effluent percent                     |           100 | False                   |                   1   | exact                                                     |
| inorganic particles                             | exact        | inorganic particles                             |           100 | False                   |                   1   | exact                                                     |
| isolation and growth condition                  | exact        | isolation and growth condition                  |           100 | True                    |                   1   | exact                                                     |
| known pathogenicity                             | exact        | known pathogenicity                             |           100 | False                   |                   1   | exact                                                     |
| library reads sequenced                         | exact        | library reads sequenced                         |           100 | False                   |                   1   | exact                                                     |
| library screening strategy                      | exact        | library screening strategy                      |           100 | False                   |                   1   | exact                                                     |
| library size                                    | exact        | library size                                    |           100 | False                   |                   1   | exact                                                     |
| library vector                                  | exact        | library vector                                  |           100 | False                   |                   1   | exact                                                     |
| light intensity                                 | exact        | light intensity                                 |           100 | False                   |                   1   | exact                                                     |
| light regimen                                   | exact        | light regimen                                   |           100 | False                   |                   1   | exact                                                     |
| light type                                      | exact        | light type                                      |           100 | False                   |                   1   | exact                                                     |
| link to classification information              | exact        | link to classification information              |           100 | False                   |                   1   | exact                                                     |
| link to climate information                     | exact        | link to climate information                     |           100 | False                   |                   1   | exact                                                     |
| links to additional analysis                    | exact        | links to additional analysis                    |           100 | False                   |                   1   | exact                                                     |
| liver disorder                                  | exact        | liver disorder                                  |           100 | False                   |                   1   | exact                                                     |
| local environmental context                     | exact        | local environmental context                     |           100 | False                   |                   1   | exact                                                     |
| lung/nose-throat disorder                       | fuzzy        | nose throat disorder                            |            95 | False                   |                   0.7 | right is a substring of left                              |
| lung/pulmonary disorder                         | exact        | lung/pulmonary disorder                         |           100 | False                   |                   1   | exact                                                     |
| magnesium                                       | exact        | magnesium                                       |           100 | False                   |                   1   | exact                                                     |
| major diet change in last six months            | exact        | major diet change in last six months            |           100 | False                   |                   1   | exact                                                     |
| mean annual and seasonal precipitation          | fuzzy        | mean seasonal precipitation                     |            95 | False                   |                   0.3 | left and right two words apart                            |
| mean annual and seasonal temperature            | fuzzy        | mean seasonal temperature                       |            95 | False                   |                   0.3 | left and right two words apart                            |
| mean friction velocity                          | exact        | mean friction velocity                          |           100 | False                   |                   1   | exact                                                     |
| mean peak friction velocity                     | exact        | mean peak friction velocity                     |           100 | False                   |                   1   | exact                                                     |
| mechanical damage                               | exact        | mechanical damage                               |           100 | False                   |                   1   | exact                                                     |
| medical history performed                       | exact        | medical history performed                       |           100 | False                   |                   1   | exact                                                     |
| menarche                                        | exact        | menarche                                        |           100 | False                   |                   1   | exact                                                     |
| menopause                                       | exact        | menopause                                       |           100 | False                   |                   1   | exact                                                     |
| methane                                         | exact        | methane                                         |           100 | False                   |                   1   | exact                                                     |
| microbial biomass                               | exact        | microbial biomass                               |           100 | False                   |                   1   | exact                                                     |
| microbial biomass method                        | exact        | microbial biomass method                        |           100 | False                   |                   1   | exact                                                     |
| mineral nutrient regimen                        | exact        | mineral nutrient regimen                        |           100 | False                   |                   1   | exact                                                     |
| multiplex identifiers                           | exact        | multiplex identifiers                           |           100 | False                   |                   1   | exact                                                     |
| n-alkanes                                       | exact        | n-alkanes                                       |           100 | False                   |                   1   | exact                                                     |
| negative control type                           | exact        | negative control type                           |           100 | False                   |                   1   | exact                                                     |
| nitrate                                         | exact        | nitrate                                         |           100 | True                    |                   1   | exact                                                     |
| nitrite                                         | exact        | nitrite                                         |           100 | False                   |                   1   | exact                                                     |
| nitrogen                                        | exact        | nitrogen                                        |           100 | True                    |                   1   | exact                                                     |
| non-mineral nutrient regimen                    | exact        | non-mineral nutrient regimen                    |           100 | False                   |                   1   | exact                                                     |
| nucleic acid amplification                      | exact        | nucleic acid amplification                      |           100 | False                   |                   1   | exact                                                     |
| nucleic acid extraction                         | exact        | nucleic acid extraction                         |           100 | False                   |                   1   | exact                                                     |
| number of replicons                             | exact        | number of replicons                             |           100 | False                   |                   1   | exact                                                     |
| number of standard tRNAs extracted              | exact        | number of standard tRNAs extracted              |           100 | False                   |                   1   | exact                                                     |
| observed biotic relationship                    | exact        | observed biotic relationship                    |           100 | True                    |                   1   | exact                                                     |
| occupancy at sampling                           | exact        | occupancy at sampling                           |           100 | False                   |                   1   | exact                                                     |
| occupant density at sampling                    | exact        | occupant density at sampling                    |           100 | True                    |                   1   | exact                                                     |
| organic carbon                                  | exact        | organic carbon                                  |           100 | False                   |                   1   | exact                                                     |
| organic matter                                  | exact        | organic matter                                  |           100 | False                   |                   1   | exact                                                     |
| organic nitrogen                                | exact        | organic nitrogen                                |           100 | False                   |                   1   | exact                                                     |
| organic particles                               | exact        | organic particles                               |           100 | False                   |                   1   | exact                                                     |
| organism count                                  | exact        | organism count                                  |           100 | False                   |                   1   | exact                                                     |
| oxygen                                          | exact        | oxygen                                          |           100 | True                    |                   1   | exact                                                     |
| oxygenation status of sample                    | exact        | oxygenation status of sample                    |           100 | False                   |                   1   | exact                                                     |
| pH                                              | exact        | pH                                              |           100 | False                   |                   1   | exact                                                     |
| pH method                                       | exact        | pH method                                       |           100 | False                   |                   1   | exact                                                     |
| pH regimen                                      | exact        | pH regimen                                      |           100 | False                   |                   1   | exact                                                     |
| particulate organic carbon                      | exact        | particulate organic carbon                      |           100 | False                   |                   1   | exact                                                     |
| particulate organic nitrogen                    | exact        | particulate organic nitrogen                    |           100 | False                   |                   1   | exact                                                     |
| pcr conditions                                  | exact        | pcr conditions                                  |           100 | False                   |                   1   | exact                                                     |
| pcr primers                                     | exact        | pcr primers                                     |           100 | False                   |                   1   | exact                                                     |
| perturbation                                    | exact        | perturbation                                    |           100 | False                   |                   1   | exact                                                     |
| pesticide regimen                               | exact        | pesticide regimen                               |           100 | False                   |                   1   | exact                                                     |
| petroleum hydrocarbon                           | exact        | petroleum hydrocarbon                           |           100 | False                   |                   1   | exact                                                     |
| phaeopigments                                   | exact        | phaeopigments                                   |           100 | False                   |                   1   | exact                                                     |
| phosphate                                       | exact        | phosphate                                       |           100 | False                   |                   1   | exact                                                     |
| phospholipid fatty acid                         | exact        | phospholipid fatty acid                         |           100 | False                   |                   1   | exact                                                     |
| photon flux                                     | exact        | photon flux                                     |           100 | False                   |                   1   | exact                                                     |
| plant growth medium                             | exact        | plant growth medium                             |           100 | False                   |                   1   | exact                                                     |
| plant product                                   | exact        | plant product                                   |           100 | False                   |                   1   | exact                                                     |
| plant sex                                       | exact        | plant sex                                       |           100 | False                   |                   1   | exact                                                     |
| plant structure                                 | exact        | plant structure                                 |           100 | False                   |                   1   | exact                                                     |
| ploidy                                          | exact        | ploidy                                          |           100 | False                   |                   1   | exact                                                     |
| pollutants                                      | exact        | pollutants                                      |           100 | False                   |                   1   | exact                                                     |
| pooling of DNA extracts (if done)               | exact        | pooling of DNA extracts (if done)               |           100 | False                   |                   1   | exact                                                     |
| positive control type                           | exact        | positive control type                           |           100 | False                   |                   1   | exact                                                     |
| potassium                                       | exact        | potassium                                       |           100 | False                   |                   1   | exact                                                     |
| pre-treatment                                   | exact        | pre-treatment                                   |           100 | True                    |                   1   | exact                                                     |
| predicted genome structure                      | exact        | predicted genome structure                      |           100 | False                   |                   1   | exact                                                     |
| predicted genome type                           | exact        | predicted genome type                           |           100 | False                   |                   1   | exact                                                     |
| pregnancy                                       | exact        | pregnancy                                       |           100 | False                   |                   1   | exact                                                     |
| presence of pets or farm animals                | exact        | presence of pets or farm animals                |           100 | False                   |                   1   | exact                                                     |
| pressure                                        | exact        | pressure                                        |           100 | False                   |                   1   | exact                                                     |
| primary production                              | exact        | primary production                              |           100 | False                   |                   1   | exact                                                     |
| primary treatment                               | exact        | primary treatment                               |           100 | False                   |                   1   | exact                                                     |
| profile position                                | exact        | profile position                                |           100 | False                   |                   1   | exact                                                     |
| project name                                    | exact        | project name                                    |           100 | False                   |                   1   | exact                                                     |
| propagation                                     | exact        | propagation                                     |           100 | False                   |                   1   | exact                                                     |
| radiation regimen                               | exact        | radiation regimen                               |           100 | False                   |                   1   | exact                                                     |
| rainfall regimen                                | exact        | rainfall regimen                                |           100 | False                   |                   1   | exact                                                     |
| reactor type                                    | exact        | reactor type                                    |           100 | False                   |                   1   | exact                                                     |
| reassembly post binning                         | exact        | reassembly post binning                         |           100 | False                   |                   1   | exact                                                     |
| redox potential                                 | exact        | redox potential                                 |           100 | False                   |                   1   | exact                                                     |
| reference database(s)                           | exact        | reference database(s)                           |           100 | False                   |                   1   | exact                                                     |
| reference for biomaterial                       | exact        | reference for biomaterial                       |           100 | True                    |                   1   | exact                                                     |
| relationship to oxygen                          | exact        | relationship to oxygen                          |           100 | False                   |                   1   | exact                                                     |
| relative air humidity                           | exact        | relative air humidity                           |           100 | False                   |                   1   | exact                                                     |
| relevant electronic resources                   | exact        | relevant electronic resources                   |           100 | False                   |                   1   | exact                                                     |
| relevant standard operating procedures          | exact        | relevant standard operating procedures          |           100 | False                   |                   1   | exact                                                     |
| rooting conditions                              | exact        | rooting conditions                              |           100 | False                   |                   1   | exact                                                     |
| rooting medium carbon                           | exact        | rooting medium carbon                           |           100 | False                   |                   1   | exact                                                     |
| rooting medium macronutrients                   | exact        | rooting medium macronutrients                   |           100 | False                   |                   1   | exact                                                     |
| rooting medium micronutrients                   | exact        | rooting medium micronutrients                   |           100 | False                   |                   1   | exact                                                     |
| rooting medium organic supplements              | exact        | rooting medium organic supplements              |           100 | False                   |                   1   | exact                                                     |
| rooting medium pH                               | exact        | rooting medium pH                               |           100 | False                   |                   1   | exact                                                     |
| rooting medium regulators                       | exact        | rooting medium regulators                       |           100 | False                   |                   1   | exact                                                     |
| rooting medium solidifier                       | exact        | rooting medium solidifier                       |           100 | False                   |                   1   | exact                                                     |
| salinity                                        | exact        | salinity                                        |           100 | True                    |                   1   | exact                                                     |
| salinity method                                 | fuzzy        | salinity_meth                                   |            92 | False                   |                   0.7 | right is a substring of left                              |
| salt regimen                                    | exact        | salt regimen                                    |           100 | False                   |                   1   | exact                                                     |
| sample capture status                           | exact        | sample capture status                           |           100 | True                    |                   1   | exact                                                     |
| sample collection device                        | exact        | sample collection device                        |           100 | True                    |                   1   | exact                                                     |
| sample collection device or method              | fuzzy        | sample collection device                        |            95 | True                    |                   0.3 | right is a substring of left, but also matched elsewhere  |
| sample collection method                        | exact        | sample collection method                        |           100 | False                   |                   1   | exact                                                     |
| sample disease stage                            | exact        | sample disease stage                            |           100 | True                    |                   1   | exact                                                     |
| sample material processing                      | exact        | sample material processing                      |           100 | True                    |                   1   | exact                                                     |
| sample size sorting method                      | exact        | sample size sorting method                      |           100 | False                   |                   1   | exact                                                     |
| sample storage conditions                       | fuzzy        | storage conditions                              |            95 | True                    |                   0.3 | right is a substring of left, but also matched elsewhere  |
| sample storage duration                         | exact        | sample storage duration                         |           100 | False                   |                   1   | exact                                                     |
| sample storage location                         | exact        | sample storage location                         |           100 | False                   |                   1   | exact                                                     |
| sample storage temperature                      | exact        | sample storage temperature                      |           100 | False                   |                   1   | exact                                                     |
| sample transportation temperature               | fuzzy        | sample transport temperature                    |            91 | False                   |                   0.7 | left and right one word apart                             |
| sample volume or weight for DNA extraction      | exact        | sample volume or weight for DNA extraction      |           100 | True                    |                   1   | exact                                                     |
| sample weight for DNA extraction                | fuzzy        | sample volume or weight for DNA extraction      |            95 | True                    |                   0.5 | left and right one word apart, but also matched elsewhere |
| seasonal environment                            | exact        | seasonal environment                            |           100 | False                   |                   1   | exact                                                     |
| secondary treatment                             | exact        | secondary treatment                             |           100 | False                   |                   1   | exact                                                     |
| sequence quality check                          | exact        | sequence quality check                          |           100 | False                   |                   1   | exact                                                     |
| sequencing method                               | exact        | sequencing method                               |           100 | False                   |                   1   | exact                                                     |
| sewage type                                     | exact        | sewage type                                     |           100 | False                   |                   1   | exact                                                     |
| sexual activity                                 | exact        | sexual activity                                 |           100 | False                   |                   1   | exact                                                     |
| silicate                                        | exact        | silicate                                        |           100 | False                   |                   1   | exact                                                     |
| similarity search method                        | exact        | similarity search method                        |           100 | False                   |                   1   | exact                                                     |
| size fraction selected                          | exact        | size fraction selected                          |           100 | False                   |                   1   | exact                                                     |
| slope aspect                                    | exact        | slope aspect                                    |           100 | False                   |                   1   | exact                                                     |
| slope gradient                                  | exact        | slope gradient                                  |           100 | False                   |                   1   | exact                                                     |
| sludge retention time                           | exact        | sludge retention time                           |           100 | False                   |                   1   | exact                                                     |
| smoker                                          | exact        | smoker                                          |           100 | False                   |                   1   | exact                                                     |
| sodium                                          | exact        | sodium                                          |           100 | False                   |                   1   | exact                                                     |
| soil horizon                                    | exact        | soil horizon                                    |           100 | False                   |                   1   | exact                                                     |
| soil horizon method                             | fuzzy        | horizon method                                  |            95 | False                   |                   0.7 | right is a substring of left                              |
| soil pH                                         | exact        | soil pH                                         |           100 | False                   |                   1   | exact                                                     |
| soil texture method                             | exact        | soil texture method                             |           100 | False                   |                   1   | exact                                                     |
| soil type                                       | exact        | soil type                                       |           100 | False                   |                   1   | exact                                                     |
| soil type method                                | exact        | soil type method                                |           100 | False                   |                   1   | exact                                                     |
| soil water content                              | fuzzy        | water content                                   |            95 | True                    |                   0.3 | right is a substring of left, but also matched elsewhere  |
| soil_taxonomic/FAO classification               | exact        | soil_taxonomic/FAO classification               |           100 | False                   |                   1   | exact                                                     |
| soil_taxonomic/local classification             | exact        | soil_taxonomic/local classification             |           100 | False                   |                   1   | exact                                                     |
| soil_taxonomic/local classification method      | exact        | soil_taxonomic/local classification method      |           100 | False                   |                   1   | exact                                                     |
| solar irradiance                                | exact        | solar irradiance                                |           100 | False                   |                   1   | exact                                                     |
| soluble inorganic material                      | exact        | soluble inorganic material                      |           100 | False                   |                   1   | exact                                                     |
| soluble organic material                        | exact        | soluble organic material                        |           100 | False                   |                   1   | exact                                                     |
| soluble reactive phosphorus                     | exact        | soluble reactive phosphorus                     |           100 | False                   |                   1   | exact                                                     |
| sorting technology                              | exact        | sorting technology                              |           100 | False                   |                   1   | exact                                                     |
| source material identifiers                     | exact        | source material identifiers                     |           100 | False                   |                   1   | exact                                                     |
| source of UViGs                                 | exact        | source of UViGs                                 |           100 | False                   |                   1   | exact                                                     |
| space typical state                             | exact        | space typical state                             |           100 | False                   |                   1   | exact                                                     |
| special diet                                    | exact        | special diet                                    |           100 | False                   |                   1   | exact                                                     |
| standing water regimen                          | exact        | standing water regimen                          |           100 | False                   |                   1   | exact                                                     |
| study completion status                         | exact        | study completion status                         |           100 | False                   |                   1   | exact                                                     |
| subspecific genetic lineage                     | exact        | subspecific genetic lineage                     |           100 | True                    |                   1   | exact                                                     |
| subspecific genetic lineage name                | fuzzy        | subspecific genetic lineage                     |            95 | True                    |                   0.3 | right is a substring of left, but also matched elsewhere  |
| subspecific genetic lineage rank                | fuzzy        | subspecific genetic lineage                     |            95 | True                    |                   0.3 | right is a substring of left, but also matched elsewhere  |
| substructure type                               | exact        | substructure type                               |           100 | False                   |                   1   | exact                                                     |
| sulfate                                         | exact        | sulfate                                         |           100 | False                   |                   1   | exact                                                     |
| sulfide                                         | exact        | sulfide                                         |           100 | False                   |                   1   | exact                                                     |
| surface air contaminant                         | harmonised   | surface-air contaminant                         |           100 | False                   |                   1   | very_close                                                |
| surface humidity                                | exact        | surface humidity                                |           100 | False                   |                   1   | exact                                                     |
| surface material                                | exact        | surface material                                |           100 | False                   |                   1   | exact                                                     |
| surface moisture                                | exact        | surface moisture                                |           100 | False                   |                   1   | exact                                                     |
| surface moisture pH                             | exact        | surface moisture pH                             |           100 | False                   |                   1   | exact                                                     |
| surface temperature                             | exact        | surface temperature                             |           100 | False                   |                   1   | exact                                                     |
| suspended particulate matter                    | exact        | suspended particulate matter                    |           100 | False                   |                   1   | exact                                                     |
| suspended solids                                | exact        | suspended solids                                |           100 | False                   |                   1   | exact                                                     |
| tRNA extraction software                        | exact        | tRNA extraction software                        |           100 | False                   |                   1   | exact                                                     |
| target gene                                     | exact        | target gene                                     |           100 | False                   |                   1   | exact                                                     |
| target subfragment                              | exact        | target subfragment                              |           100 | False                   |                   1   | exact                                                     |
| taxonomic classification                        | exact        | taxonomic classification                        |           100 | False                   |                   1   | exact                                                     |
| taxonomic identity marker                       | exact        | taxonomic identity marker                       |           100 | False                   |                   1   | exact                                                     |
| temperature                                     | exact        | temperature                                     |           100 | True                    |                   1   | exact                                                     |
| tertiary treatment                              | exact        | tertiary treatment                              |           100 | False                   |                   1   | exact                                                     |
| tidal stage                                     | exact        | tidal stage                                     |           100 | False                   |                   1   | exact                                                     |
| time since last toothbrushing                   | exact        | time since last toothbrushing                   |           100 | False                   |                   1   | exact                                                     |
| time since last wash                            | exact        | time since last wash                            |           100 | False                   |                   1   | exact                                                     |
| tissue culture growth media                     | exact        | tissue culture growth media                     |           100 | True                    |                   1   | exact                                                     |
| total carbon                                    | exact        | total carbon                                    |           100 | False                   |                   1   | exact                                                     |
| total depth of water column                     | exact        | total depth of water column                     |           100 | False                   |                   1   | exact                                                     |
| total dissolved nitrogen                        | exact        | total dissolved nitrogen                        |           100 | False                   |                   1   | exact                                                     |
| total inorganic nitrogen                        | exact        | total inorganic nitrogen                        |           100 | False                   |                   1   | exact                                                     |
| total nitrogen method                           | fuzzy        | total nitrogen content method                   |            95 | False                   |                   0.7 | left and right one word apart                             |
| total organic carbon                            | exact        | total organic carbon                            |           100 | False                   |                   1   | exact                                                     |
| total particulate carbon                        | exact        | total particulate carbon                        |           100 | False                   |                   1   | exact                                                     |
| total phosphate                                 | exact        | total phosphate                                 |           100 | False                   |                   1   | exact                                                     |
| total phosphorus                                | exact        | total phosphorus                                |           100 | False                   |                   1   | exact                                                     |
| travel outside the country in last six months   | exact        | travel outside the country in last six months   |           100 | True                    |                   1   | exact                                                     |
| trophic level                                   | exact        | trophic level                                   |           100 | False                   |                   1   | exact                                                     |
| turbidity                                       | exact        | turbidity                                       |           100 | False                   |                   1   | exact                                                     |
| twin sibling presence                           | exact        | twin sibling presence                           |           100 | False                   |                   1   | exact                                                     |
| typical occupant density                        | exact        | typical occupant density                        |           100 | False                   |                   1   | exact                                                     |
| urine/collection method                         | exact        | urine/collection method                         |           100 | False                   |                   1   | exact                                                     |
| urine/kidney disorder                           | exact        | urine/kidney disorder                           |           100 | False                   |                   1   | exact                                                     |
| urine/urogenital tract disorder                 | exact        | urine/urogenital tract disorder                 |           100 | False                   |                   1   | exact                                                     |
| urogenital disorder                             | exact        | urogenital disorder                             |           100 | False                   |                   1   | exact                                                     |
| ventilation rate                                | exact        | ventilation rate                                |           100 | False                   |                   1   | exact                                                     |
| ventilation type                                | exact        | ventilation type                                |           100 | False                   |                   1   | exact                                                     |
| viral identification software                   | exact        | viral identification software                   |           100 | False                   |                   1   | exact                                                     |
| virus enrichment approach                       | exact        | virus enrichment approach                       |           100 | False                   |                   1   | exact                                                     |
| volatile organic compounds                      | exact        | volatile organic compounds                      |           100 | False                   |                   1   | exact                                                     |
| wastewater type                                 | exact        | wastewater type                                 |           100 | False                   |                   1   | exact                                                     |
| water content                                   | exact        | water content                                   |           100 | True                    |                   1   | exact                                                     |
| water content method                            | exact        | water content method                            |           100 | False                   |                   1   | exact                                                     |
| water current                                   | exact        | water current                                   |           100 | False                   |                   1   | exact                                                     |
| water temperature regimen                       | exact        | water temperature regimen                       |           100 | False                   |                   1   | exact                                                     |
| watering regimen                                | exact        | watering regimen                                |           100 | False                   |                   1   | exact                                                     |
| weight loss in last three months                | exact        | weight loss in last three months                |           100 | False                   |                   1   | exact                                                     |
| wind direction                                  | exact        | wind direction                                  |           100 | False                   |                   1   | exact                                                     |
| wind speed                                      | exact        | wind speed                                      |           100 | False                   |                   1   | exact                                                     |
