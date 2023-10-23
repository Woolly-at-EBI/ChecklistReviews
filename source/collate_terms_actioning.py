#!/usr/bin/env python3
"""Script of collate_terms_actioning.py is to collate terms for further actioning

___author___ = "woollard@ebi.ac.uk"
___start_date___ = 2023-10-17
__docformat___ = 'reStructuredText'
chmod a+x collated_terms_actioning.py
"""

import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
import re
# from clean_terms import clean_list_ena_rules
from analyse_mixs import *
from mixs import generate_mixs6_object, generate_ena_object
datadir = "/Users/woollard/projects/ChecklistReviews/data/"

def get_input_data():
    """"""
    ic()
    input_spreadsheet = datadir + "all_terms_matches_ena2mixs.xlsx"
    #all_terms_matches_mixs2ena
    df_ena2mixs = pd.read_excel(input_spreadsheet, sheet_name="all_terms_matches_ena2mixs")
    #ic(df_ena2mixs.head())

    df_mixs2ena = pd.read_excel(input_spreadsheet, sheet_name='all_terms_matches_mixs2ena')
    #ic(df_mixs2ena.head())
    return df_ena2mixs, df_mixs2ena

def process_straight_forward_terms(df_ena2mixs, df_mixs2ena):
    """

    :param df_ena2mixs:
    :param df_mixs2ena:
    :return: the same dataframes, but removed the easy to process terms,
             + stats
    """
    stats_dict = {}
    #ic(df_ena2mixs)
    stats_dict['total_ena'] = len(df_ena2mixs)
    stats_dict['total_mixs'] = len(df_mixs2ena)

    stats_dict['exact_matches'] = df_ena2mixs.query('match_type == "exact"')['left_term'].tolist()
    stats_dict['uniq2ena'] = df_ena2mixs.query('match_type == "none"')['left_term'].tolist()
    stats_dict['harmonised_ena'] = df_ena2mixs.query('match_type == "harmonised"')['left_term'].tolist()
    stats_dict['harmonised_mixs'] = df_ena2mixs.query('match_type == "harmonised"')['match in MIXS'].tolist()
    df_ena2mixs = df_ena2mixs.query('match_type not in  ["exact", "harmonised", "none"]')
    #ic(df_ena2mixs)
    df_mixs2ena = df_mixs2ena.query('match_type not in  ["exact", "harmonised"]')
    #ic(df_mixs2ena)
    return df_ena2mixs, df_mixs2ena, stats_dict
def process_fuzzy_terms(df_ena2mixs, df_mixs2ena, stats_dict):
    """

    :param df_ena2mixs:
    :param df_mixs2ena:
    :param stats_dict:
    :return:
    """
    #ic(len(df_ena2mixs))


    ic(df_ena2mixs['mapping_recommend'].value_counts())
    #ic(df_ena2mixs.query('mapping_recommend == False').head(5))
    stats_dict['uniq2ena'].extend(df_ena2mixs.query('mapping_recommend == False')['left_term'].tolist())
    #ic(stats_dict['uniq2ena'])
    df_ena2mixs = df_ena2mixs.query('mapping_recommend != False')
    ic(len(df_ena2mixs))
    stats_dict['harmonised_ena'].extend(df_ena2mixs.query('mapping_recommend == True')['left_term'].tolist())
    stats_dict['harmonised_mixs'].extend(df_ena2mixs.query('mapping_recommend == True')['match in MIXS'].tolist())
    df_ena2mixs = df_ena2mixs.query('mapping_recommend != True')
    df_mixs2ena = df_mixs2ena.query('mapping_recommend != True')

    stats_dict['unsure_ena'] = df_ena2mixs.query('mapping_recommend in ["PARTIAL","UNSURE"]')['left_term'].tolist()
    stats_dict['unsure_mixs'] = df_ena2mixs.query('mapping_recommend in ["PARTIAL","UNSURE"]')['match in MIXS'].tolist()
    stats_dict['unsure_mixs_set'] = set(stats_dict['unsure_mixs'])
    #ic(stats_dict['unsure_mixs_set'])
    df_ena2mixs = df_ena2mixs.query('mapping_recommend not in ["PARTIAL","UNSURE"]')
    ic(len(df_ena2mixs))
    tmp_set = set(df_mixs2ena['left_term'].tolist())  # this is what is left
    tmp_set.discard(set(stats_dict['unsure_mixs']))
    stats_dict['uniq2mixs']  = list(tmp_set)

    return df_ena2mixs, df_mixs2ena, stats_dict

def create_annotated_list(list_length, annotation):
    """
    creates a list all populated withe supplied annotation
    :param list_length:
    :param annotation:
    :return:
    """
    my_list = []
    for i in range(list_length):
        my_list.append(annotation)
    return my_list

def assess2lists4left_rules(left_list, right_list, action_list):
    """
    asssumes that all the lists are the same length!
    :param left_list:
    :param right_list:
    :param action_list:
    :return:
    """
    for i in range(len(left_list)):
        found_US = False
        if "_" in left_list[i]:
            #ic(f"{left_list[i]} contains '_'")
            action_list[i] = "remove '_' from the ENA term name and then map them"
            found_US = True
        if bool(re.match(r'[A-Z]', left_list[i])):
            #ic(f"{left_list[i]} contains upper case chars")
            if found_US:
               action_list[i] = "remove '_' from the ENA term name, make lower case; then map them"
            else:
                action_list[i] = "make ENA term lower case; then map them"

    return action_list

def mixs_package_freq_annotate(my_list):
    """
    :param my_list:
    :return: package_freq_annotated_list
    """
    mixs_v6_obj, mixs_v6_dict, linkml_mixs_dict = generate_mixs6_object()

    mix_v6_terms_by_freq = mixs_v6_obj.get_terms_with_freq()
    #ic(mix_v6_terms_by_freq)

    package_freq_annotated_list = []
    for term in my_list:
        package_freq_annotated_list.append(mix_v6_terms_by_freq[term])

    return package_freq_annotated_list

def mixs_package_cat_annotate(all_mixs_term_list):
    mixs_v6_obj, mixs_v6_dict, linkml_mixs_dict = generate_mixs6_object()
    mixs_package_cat_list = []
    term_dict = mixs_v6_obj.get_term_dict()
    for term in all_mixs_term_list:
        # ic(term)
        # ic(term_dict[term]['package_category_set'])
        package_set = term_dict[term]['package_category_set']
        mixs_package_cat_list.append(', '.join(sorted(list(package_set))))

    return mixs_package_cat_list

def mixs_description_annotate(all_mixs_term_list):
    mixs_v6_obj, mixs_v6_dict, linkml_mixs_dict = generate_mixs6_object()
    annotation_list = []
    term_dict = mixs_v6_obj.get_term_dict()
    for term in all_mixs_term_list:
        ic(term)
        ic(term_dict[term])
        annotation_list.append(term_dict[term]['description'])
    return annotation_list

def ena_description_annotate(all_ena_term_list):
    mixs_v6_obj, mixs_v6_dict, linkml_mixs_dict = generate_mixs6_object()
    ena_cl_obj, ena_cl_dict = generate_ena_object()
    annotation_list = []
    term_dict = ena_cl_obj.get_term_dict()
    ic(all_ena_term_list)
    count = 0
    for term in all_ena_term_list:
        ic(f"{count} {term}")
        if term in term_dict:
            ic(f"INFO {term} IS present in term_dict {term_dict[term]['description']}")
            annotation_list.append(term_dict[term]['description'])
        else:
            ic(f"ERROR {term} not present in term_dict")
            annotation_list.append("no description")
        count += 1

    #ic(annotation_list)
    sys.exit()
    return annotation_list


def generatePrioritisingSpreadsheet(stats_dict,prioritised_xlsx_filename):
    """
    Adding the terms to a dataframe and then write the dataframe to a spreadsheet


    :param stats_dict:
    :param prioritised_xlsx_filename:
    :return: the data frame
    """

    #improved changes to ENA terms to start with
    ic()


    # mapping "harmonised"
    priority_list = create_annotated_list(len(stats_dict['harmonised_ena']),"high")
    action_list = create_annotated_list(len(stats_dict['harmonised_ena']), "map the terms")
    comment_list = create_annotated_list(len(stats_dict['harmonised_ena']), "these are the harmonised terms")
    action_list = assess2lists4left_rules(stats_dict['harmonised_ena'], stats_dict['harmonised_mixs'], action_list)

    harmonised_df = pd.DataFrame({'ENA_term': stats_dict['harmonised_ena'], 'MIXSv6_term': stats_dict['harmonised_mixs'],
                       'priority': priority_list, 'action': action_list, 'comment': comment_list})


    # actions for the unsures
    priority_list = create_annotated_list(len(stats_dict['unsure_ena']),"medium")
    action_list = create_annotated_list(len(stats_dict['unsure_ena']), "investigate and decide if valid mapping")
    comment_list = create_annotated_list(len(stats_dict['unsure_ena']), "these are the unsure terms")
    unsure_df = pd.DataFrame({'ENA_term': stats_dict['unsure_ena'], 'MIXSv6_term': stats_dict['unsure_mixs'],
                        'priority': priority_list, 'action': action_list, 'comment': comment_list})

    # actions for uniq 2 mixs terms
    priority_list = create_annotated_list(len(stats_dict['uniq2mixs']), "low")
    comment_list = create_annotated_list(len(stats_dict['uniq2mixs']), "automatically suggested terms in the ENA_term columns")
    action_list = create_annotated_list(len(stats_dict['uniq2mixs']), "create new ENA terms")



    ena_term_list = clean_list_ena_rules(stats_dict['uniq2mixs'])
    ena_term_list = [s.replace('_', ' ') for s in ena_term_list]
    uniqmixs_df = pd.DataFrame({'ENA_term': ena_term_list, 'MIXSv6_term': stats_dict['uniq2mixs'],
                        'priority': priority_list, 'action': action_list, 'comment': comment_list})

    df = pd.concat([harmonised_df, unsure_df, uniqmixs_df])
    ic(df.query('priority == "high"').sample(3))
    ic(df.query('priority == "medium"').sample(3))
    ic(df.query('priority == "low"').sample(3))

    #adding checklist/package frequency
    all_mixs_term_list = df['MIXSv6_term'].values.tolist()
    mixs_package_freq_list = mixs_package_freq_annotate(all_mixs_term_list)
    df['mixs_package_freq'] = pd.Series(mixs_package_freq_list)

    mixs_package_cat_list = mixs_package_cat_annotate(all_mixs_term_list)
    df['mixs_package_categories'] = pd.Series(mixs_package_cat_list)
    ic(df.sample(n=4))


    my_mixslist = 'depth£salinity£sample collection device£size-fraction lower threshold£size-fraction upper threshold£temperature£host_family_relationship£surface-air contaminant£x_16s_recover_software£observed biotic relationship£geographic location (country and/or sea,region)£tissue culture growth media£mean seasonal precipitation£mean seasonal temperature£biological sample replicate£salinity_meth£sample collection device£storage conditions£sample transport temperature£sample volume or weight for DNA extraction£horizon method£water content£storage conditions£nitrogen£total nitrogen content method£total organic carbon method£geographic location (latitude and longitude)£geographic location (latitude and longitude)£geographic location (latitude and longitude)£geographic location (latitude and longitude)£assembly quality£experimental factor£experimental factor£experimental factor£experimental factor£experimental factor£geographic location (latitude and longitude)£geographic location (latitude and longitude)£host body habitat£enrichment protocol£amount or size of sample collected£amniotic fluid/foetal health status£amount or size of sample collected£amount or size of sample collected£amount or size of sample collected£Food_source£subspecific genetic lineage£subspecific genetic lineage£mean annual temperature£alkalinity method£food packing medium£bedroom count£sample pooling£wall construction type£specific intended consumer£sample subtype£mean annual precipitation£purchase date£fermentation headspace oxygen£shading device type£farm equipment sanitization frequency£microbial starter organism count£specifications£wall signs of water/mold£spike-in with antibiotics£culture result organism£window condition£benzene£escalator count£food stored by consumer (storage temperature)£biocide£shading device location£cooling system identifier£host of the symbiotic host common name£quadrant position£API gravity£food distribution point geographic location£nose throat disorder£number of pets£source rock geological age£window vertical position£fireplace type£heating delivery locations£ceiling finish material£horizon method£production rate£door type£number of houseplants£study incubation temperature£non_mineral_nutr_regm£number of samples collected£floor age£organism count qPCR information£rooms connected by a doorway£host of the symbiotic host family relationship£farm watering water source£environmental feature adjacent water source£food package capacity£has_unit£host of the symbiotic host genotype£weekday£temperature outside house£wall location£room volume£architectural structure£door type, composite£secondary and tertiary recovery methods and start date£previous_land_use_meth£adjacent rooms£door area or size£horizon£relative location of sample£room architectural elements£host of the symbiotic host phenotype£wall surface treatment£mode of transmission£frequency of cooking£visual media£rooms that are on the same hallway£host of the symbiotic host environemental medium£total nitrogen concentration£wall area£tot_car£animal feeding equipment£sample storage solution£orientations of exterior wall£specific humidity£food distribution point geographic location (city)£seasonal use£crop yield£material of contact prior to food packaging£elevator count£floor area£built structure setting£symbiotic host organism life cycle type£preservative added to sample£culture target microbial analyte£facility type£host dependence£furniture£growth medium£samp_stor_temp£water feature type£drawings£food product name legal status£food production system characteristics£date last rain£total iron£room door distance£sample type£fertilizer administration£microbial_biomass_meth£room type£window location£dissolved iron£ceiling type£volatile fatty acids£time-course duration£fertilizer administration date£viscosity£single_cell_lysis_prot£sampling room sterilization method£door direction of opening£last time swept/mopped/vacuumed£average temperature£exposed pipes£source rock depositional environment£wall height£food quality date£fermentation pH£fermentation vessel£mechanical structure£number of contigs£tot_phos£oil water contact depth£built structure type£door type, metal£extreme weather event£food cleaning process£inside lux light£lot number£train station collection location£exposed ductwork£study design£host specificity£hygienic food production area£door material£additional info£sample transport  container£room dimensions£biocide administration method£aerospace structure£Food_Product_type£sample location condition£resins wt%£sample transport temperature£wall thermal mass£fermentation chemical additives£ceiling signs of water/mold£food contact surface£sampling time outside£fermentation chemical additives percentage£food cooking process£study treatment£purpose of sampling£window status£sample storage media£address£library preparation kit£hydrocarbon resource original pressure£microbiological culture medium£dissolved oxygen in fluids£duration of association with the host£door location£host_infra_specific_name£food product by quality£url£samp_stor_loc£window signs of water/mold£formation water salinity£library layout£window type£samp_stor_dur£mean seasonal humidity£nucleic acid extraction kit£window material£sampling day weather£basin name£spike in organism£bacteria density£porosity£sample true vertical depth subsea£window horizontal position£water feature size£collection site geographic feature£food animal antimicrobial route of administration£sample transport conditions£sample measured depth£permeability£spike-in organism count£train stop collection location£room condition£window area/size£total sulfur£amount of light£food allergen labeling£spike-in growth medium£fermentation temperature£annotation£sampling floor£farm equipment sanitization£food product type£injection water fraction£host cellular location£sample_name£injection water breakthrough date of specific well£biological sample replicate£ethylbenzene£observed host symbionts£room count£pour point£reservoir name£train line£average daily occupancy£single_cell_lysis_appr£texture_meth£host of the symbiotic host infra-specific rank£water pH£food production characteristics£food animal source sex category£soil texture classification£floor condition£food source£type of symbiosis£animal intrusion near sample source£exterior door count£food packing medium integrity£texture£door type, wood£microbial starter£sequencing location£food shipping transportation vehicle£soil conductivity£sample_collec_method£food treatment process£food animal source diet£samp_collec_device£mean seasonal precipitation£vfa in formation water£chemical treatment£door condition£door movement£interior wall condition£production labeling claims£hydrocarbon resource geological age£floor signs of water/mold£depth (TVDSS) of hydrocarbon resource temperature£photosynthetic activity method£fermentation medium£depositional environment£ceiling structure£presence of pets, animals, or insects£wall texture£sample storage device£repository name£depth (TVDSS) of hydrocarbon resource pressure£number of residents£production start date£floor thermal mass£food preservation process£sediment type£extreme weather date£sample transport duration£microbial starter NCBI taxonomy ID£observed coinfecting organisms in host of host£heating system identifier£samp_salinity£room air exchange rate£design, construction, and operation documents£Interagency Food Safety Analytics Collaboration (IFSAC) category£food animal body condition£bathroom count£tot_n_meth£spike-in with heavy metals£host of the symbiotic host subject id£handidness£has_raw_value£shading device signs of water/mold£sieving£total acid number£food animal group size£source rock kerogen type£hydrocarbon resource type£host of the symbiotic host infra-specific name£window covering£spike-in microbial strain£food product synonym£sample well name£mean seasonal temperature£ceiling texture£food ingredient£maximum occupancy£timepoint£culture result£shading device condition£gender of restroom£window open frequency£salinity_meth£sequencing kit£soil cover£ceiling condition£water production rate£season£microbial starter inoculation£food stored by consumer (storage duration)£microbial starter source£photosynthetic activity£host of the symbiont role£well identification number£floor structure£occupancy documentation£floor count£soil sediment porosity£rooms that share a wall with sampling room£sample surface moisture£water delivery frequency£wall finish material£x_16s_recover£total nitrogen content£food animal antimicrobial duration£water cut£room occupancy£sulfate in formation water£fermentation relative humidity£room location in building£toluene£area sampled size£food animal antimicrobial£host specificity or range£part of plant or animal£microbial starter preparation£hydrocarbon type produced£floor finish material£sample source material category£host of the symbiotic host gravidity£lithology£total nitrogen content method£Hazard Analysis Critical Control Points (HACCP) guide food safety term£shading device material£field name£source rock lithology£total organic carbon method£dietary claim or use£spike-in bacterial serovar or serotype£culture isolation date£room window count£frequency of cleaning£built structure age£degree of plant part maturity£environment adjacent to site£food production environmental monitoring zone£relative sampling location£sampling room ID or name£local air flow impediments£plant reproductive part£animal housing system£particle classification£asphaltenes wt%£storage conditions£height carpet fiber mat£food traceability list category£host of the symbiotic host total mass£ceiling area£Food harvesting process£has_numeric_value£plant water delivery method£taxonomy ID of DNA sample£heating system delivery method£enrichment protocol£food animal antimicrobial frequency£xylene£intended consumer£room sampling position£animal water delivery method£serovar or serotype£host of the symbiotic host taxon id£antimicrobial phenotype of spike-in bacteria£technical sample replicate£quantity purchased£fermentation time£sample collection point£biocide administration£corrosion rate at sample location£equipment shared with other farms£hydrocarbon resource original temperature£host of the symbiotic host disease status£miscellaneous parameter£water source shared£room moisture damage or mold history£food container or wrapping£average dew point£soil_text_measure£host_family_relation£outside relative humidity£hallway/corridor count£sample name£food additive£food product origin geographic location£host of the symbiotic host local environmental context£aromatics wt%£host number individual£study incubation duration£Food_source£assembly name£route of transmission£food shipping transportation method£samp_collec_method£farm equipment used£door signs of water/mold£host_infra_specific_rank£room net area£ceiling thermal mass£chemical treatment method£saturates wt%£food source age£rooms that share a door with sampling room£orientations of exterior window£food animal antimicrobial intended use'.split('£')
    my_enalist = 'Depth£Salinity£Sample Collection Device£Size Fraction Lower Threshold£Size Fraction Upper Threshold£Temperature£host family relationship£surface air contaminant£16S recovery software£biotic relationship£geographic location (country and/or sea)£growth media£mean annual and seasonal precipitation£mean annual and seasonal temperature£replicate£salinity method£sample collection device or method£sample storage conditions£sample transportation temperature£sample weight for DNA extraction£soil horizon method£soil water content£storage conditions (fresh/frozen/other)£total nitrogen£total nitrogen method£total organic C method£Latitude End£Latitude Start£Longitude End£Longitude Start£UViG assembly quality£experimental factor 1£experimental factor 2£experimental factor 3£experimental factor 4£experimental factor 5£geographic location (latitude)£geographic location (longitude)£host habitat£protocol£sample dry mass£sample health state£sample height£sample length£sample wet mass£source material description£subspecific genetic lineage name£subspecific genetic lineage rank£mean annual temperature£alkalinity method£food packing medium£bedroom count£sample pooling£wall construction type£specific intended consumer£sample subtype£mean annual precipitation£purchase date£fermentation headspace oxygen£shading device type£farm equipment sanitization frequency£microbial starter organism count£specifications£wall signs of water/mold£spike in with antibiotics£culture result organism£window condition£benzene£escalator count£food stored by consumer (storage temperature)£biocide£shading device location£cooling system identifier£host of the symbiotic host common name£quadrant position£api gravity£food distribution point geographic location£nose throat disorder£number of pets£source rock geological age£window vertical position£fireplace type£heating delivery locations£ceiling finish material£horizon method£production rate£door type£number of houseplants£study incubation temperature£non mineral nutr regm£number of samples collected£floor age£organism count qpcr information£rooms connected by a doorway£host of the symbiotic host family relationship£farm watering water source£environmental feature adjacent water source£food package capacity£has unit£host of the symbiotic host genotype£weekday£temperature outside house£wall location£room volume£architectural structure£door type, composite£secondary and tertiary recovery methods and start date£previous land use meth£adjacent rooms£door area or size£horizon£relative location of sample£room architectural elements£host of the symbiotic host phenotype£wall surface treatment£mode of transmission£frequency of cooking£visual media£rooms that are on the same hallway£host of the symbiotic host environemental medium£total nitrogen concentration£wall area£tot car£animal feeding equipment£sample storage solution£orientations of exterior wall£specific humidity£food distribution point geographic location (city)£seasonal use£crop yield£material of contact prior to food packaging£elevator count£floor area£built structure setting£symbiotic host organism life cycle type£preservative added to sample£culture target microbial analyte£facility type£host dependence£furniture£growth medium£samp stor temp£water feature type£drawings£food product name legal status£food production system characteristics£date last rain£total iron£room door distance£sample type£fertilizer administration£microbial biomass meth£room type£window location£dissolved iron£ceiling type£volatile fatty acids£time course duration£fertilizer administration date£viscosity£single cell lysis prot£sampling room sterilization method£door direction of opening£last time swept/mopped/vacuumed£average temperature£exposed pipes£source rock depositional environment£wall height£food quality date£fermentation ph£fermentation vessel£mechanical structure£number of contigs£tot phos£oil water contact depth£built structure type£door type, metal£extreme weather event£food cleaning process£inside lux light£lot number£train station collection location£exposed ductwork£study design£host specificity£hygienic food production area£door material£additional info£sample transport container£room dimensions£biocide administration method£aerospace structure£food product type£sample location condition£resins wt%£sample transport temperature£wall thermal mass£fermentation chemical additives£ceiling signs of water/mold£food contact surface£sampling time outside£fermentation chemical additives percentage£food cooking process£study treatment£purpose of sampling£window status£sample storage media£address£library preparation kit£hydrocarbon resource original pressure£microbiological culture medium£dissolved oxygen in fluids£duration of association with the host£door location£host infra specific name£food product by quality£url£samp stor loc£window signs of water/mold£formation water salinity£library layout£window type£samp stor dur£mean seasonal humidity£nucleic acid extraction kit£window material£sampling day weather£basin name£spike in organism£bacteria density£porosity£sample true vertical depth subsea£window horizontal position£water feature size£collection site geographic feature£food animal antimicrobial route of administration£sample transport conditions£sample measured depth£permeability£spike in organism count£train stop collection location£room condition£window area/size£total sulfur£amount of light£food allergen labeling£spike in growth medium£fermentation temperature£annotation£sampling floor£farm equipment sanitization£food product type£injection water fraction£host cellular location£sample name£injection water breakthrough date of specific well£biological sample replicate£ethylbenzene£observed host symbionts£room count£pour point£reservoir name£train line£average daily occupancy£single cell lysis appr£texture meth£host of the symbiotic host infra specific rank£water ph£food production characteristics£food animal source sex category£soil texture classification£floor condition£food source£type of symbiosis£animal intrusion near sample source£exterior door count£food packing medium integrity£texture£door type, wood£microbial starter£sequencing location£food shipping transportation vehicle£soil conductivity£sample collec method£food treatment process£food animal source diet£samp collec device£mean seasonal precipitation£vfa in formation water£chemical treatment£door condition£door movement£interior wall condition£production labeling claims£hydrocarbon resource geological age£floor signs of water/mold£depth (tvdss) of hydrocarbon resource temperature£photosynthetic activity method£fermentation medium£depositional environment£ceiling structure£presence of pets, animals, or insects£wall texture£sample storage device£repository name£depth (tvdss) of hydrocarbon resource pressure£number of residents£production start date£floor thermal mass£food preservation process£sediment type£extreme weather date£sample transport duration£microbial starter ncbi taxonomy id£observed coinfecting organisms in host of host£heating system identifier£samp salinity£room air exchange rate£design, construction, and operation documents£interagency food safety analytics collaboration (ifsac) category£food animal body condition£bathroom count£tot n meth£spike in with heavy metals£host of the symbiotic host subject id£handidness£has raw value£shading device signs of water/mold£sieving£total acid number£food animal group size£source rock kerogen type£hydrocarbon resource type£host of the symbiotic host infra specific name£window covering£spike in microbial strain£food product synonym£sample well name£mean seasonal temperature£ceiling texture£food ingredient£maximum occupancy£timepoint£culture result£shading device condition£gender of restroom£window open frequency£salinity meth£sequencing kit£soil cover£ceiling condition£water production rate£season£microbial starter inoculation£food stored by consumer (storage duration)£microbial starter source£photosynthetic activity£host of the symbiont role£well identification number£floor structure£occupancy documentation£floor count£soil sediment porosity£rooms that share a wall with sampling room£sample surface moisture£water delivery frequency£wall finish material£x 16s recover£total nitrogen content£food animal antimicrobial duration£water cut£room occupancy£sulfate in formation water£fermentation relative humidity£room location in building£toluene£area sampled size£food animal antimicrobial£host specificity or range£part of plant or animal£microbial starter preparation£hydrocarbon type produced£floor finish material£sample source material category£host of the symbiotic host gravidity£lithology£total nitrogen content method£hazard analysis critical control points (haccp) guide food safety term£shading device material£field name£source rock lithology£total organic carbon method£dietary claim or use£spike in bacterial serovar or serotype£culture isolation date£room window count£frequency of cleaning£built structure age£degree of plant part maturity£environment adjacent to site£food production environmental monitoring zone£relative sampling location£sampling room id or name£local air flow impediments£plant reproductive part£animal housing system£particle classification£asphaltenes wt%£storage conditions£height carpet fiber mat£food traceability list category£host of the symbiotic host total mass£ceiling area£food harvesting process£has numeric value£plant water delivery method£taxonomy id of dna sample£heating system delivery method£enrichment protocol£food animal antimicrobial frequency£xylene£intended consumer£room sampling position£animal water delivery method£serovar or serotype£host of the symbiotic host taxon id£antimicrobial phenotype of spike in bacteria£technical sample replicate£quantity purchased£fermentation time£sample collection point£biocide administration£corrosion rate at sample location£equipment shared with other farms£hydrocarbon resource original temperature£host of the symbiotic host disease status£miscellaneous parameter£water source shared£room moisture damage or mold history£food container or wrapping£average dew point£soil text measure£host family relation£outside relative humidity£hallway/corridor count£sample name£food additive£food product origin geographic location£host of the symbiotic host local environmental context£aromatics wt%£host number individual£study incubation duration£food source£assembly name£route of transmission£food shipping transportation method£samp collec method£farm equipment used£door signs of water/mold£host infra specific rank£room net area£ceiling thermal mass£chemical treatment method£saturates wt%£food source age£rooms that share a door with sampling room£orientations of exterior window£food animal antimicrobial intended use'.split('£')
    # rtn_list = mixs_package_freq_annotate(my_mixslist)
    # rtn_list = map(str, rtn_list)
    # print('\n'.join(rtn_list))
    # print("=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+" )
    # sys.exit()
    # rtn_list = mixs_package_cat_annotate(my_mixslist)
    # print('\n'.join(rtn_list))

    #rtn_list = mixs_description_annotate(my_mixslist)
    #print('\n'.join(rtn_list))

    rtn_list = ena_description_annotate(my_enalist)
    print('\n'.join(rtn_list))

    ic(f"creating {prioritised_xlsx_filename}")
    df.to_excel(prioritised_xlsx_filename, index=False)

    return df

def printStats(stats_dict):
    """

    :param stats_dict:
    :return:
    """
    ic()
    ic(stats_dict['total_ena'])
    ic(stats_dict['total_mixs'])
    ic(len(stats_dict['exact_matches']))
    ic(len(stats_dict['uniq2ena']))
    ic(len(stats_dict['uniq2mixs']))
    ic(len(stats_dict['harmonised_ena']))
    ic(len(stats_dict['harmonised_mixs']))
    ic(len(stats_dict['unsure_ena'] ))
    ic(len(set(stats_dict['unsure_mixs'])))

def main():
    df_ena2mixs, df_mixs2ena = get_input_data()
    ic(len(df_ena2mixs))
    ic(len(df_mixs2ena))
    df_ena2mixs, df_mixs2ena, stats_dict = process_straight_forward_terms(df_ena2mixs, df_mixs2ena)
    ic(len(df_ena2mixs))
    df_ena2mixs, df_mixs2ena, stats_dict = process_fuzzy_terms(df_ena2mixs, df_mixs2ena, stats_dict)
    ic(len(df_ena2mixs))
    ic(len(df_mixs2ena))
    printStats(stats_dict)

    prioritised_xlsx_filename = datadir + "ena_mixs_mapping_prioritised.xlsx"
    generatePrioritisingSpreadsheet(stats_dict,prioritised_xlsx_filename)

if __name__ == '__main__':
    ic()
    main()
