import unittest
from analyse_mixs import *


class Testpairwise_term_matches(unittest.TestCase):

    linkml_mixs_dict = parse_new_linkml()
    ena_cl_dict = get_ena_dict()
    ena_cl_obj = mixs(ena_cl_dict, "ena_cl", linkml_mixs_dict)
    my_dict_v6 = get_mixs_dict("my_dict_v6")
    mixs_v6_dict = process_mixs_dict(my_dict_v6, linkml_mixs_dict)
    mixs_v6_obj = mixs(mixs_v6_dict, "mixs_v6", linkml_mixs_dict)

    left_obj = ena_cl_obj
    right_obj = mixs_v6_obj
    pair_string = names2pair_string(left_obj.type, right_obj.type)
    pairwise_obj = pairwise_term_matches(pair_string, left_obj.get_all_term_list(), right_obj.get_all_term_list())


    def test_get_left_name(self):
        self.assertEqual(self.pairwise_obj.get_left_name(), 'ena_cl')

    def test_get_right_name(self):
        self.assertEqual(self.pairwise_obj.get_right_name(), 'mixs_v6')

    def test_unique_sorted_list(self):
        test_in = ['c', 'a', 'b']
        self.assertListEqual(self.pairwise_obj.unique_sorted_list(test_in), ['a', 'b', 'c'])

    def test_get_comparison_df(self):
        df = self.pairwise_obj.get_comparison_df()
        #ic(sorted(df.columns))
        test_columns = ['fuzzy_score', 'left_term', 'match', 'match_term_duplicated', 'match_type']
        self.assertListEqual(sorted(df.columns),test_columns)
        self.assertEqual(len(df),625)
    def test_get_left_exact_matched_list(self):
        #ic()
        test_out = sorted(
            ['HRT', 'IHMC medication code', 'MAG coverage software', 'OTU classification approach', 'OTU database',
             'OTU sequence comparison approach', 'WGA amplification approach', 'WGA amplification kit',
             'absolute air humidity', 'adapters', 'air particulate matter concentration', 'air temperature regimen',
             'alkalinity', 'alkyl diethers', 'altitude', 'aminopeptidase activity', 'ammonium', 'amniotic fluid/color',
             'amniotic fluid/foetal health status', 'amniotic fluid/gestation state',
             'amniotic fluid/maternal health status', 'amount or size of sample collected', 'ancestral data',
             'antibiotic regimen', 'assembly quality', 'assembly software', 'atmospheric data',
             'bacterial carbon production', 'bacterial production', 'bacterial respiration', 'barometric pressure',
             'binning parameters', 'binning software', 'biochemical oxygen demand', 'biological status', 'biomass',
             'biotic regimen', 'birth control', 'bishomohopanol', 'blood/blood disorder',
             'broad-scale environmental context', 'bromide', 'building occupancy type', 'building setting', 'calcium',
             'carbon dioxide', 'carbon monoxide', 'carbon/nitrogen ratio', 'chemical administration',
             'chemical mutagen', 'chemical oxygen demand', 'chimera check software', 'chloride', 'chlorophyll',
             'climate environment', 'collection date', 'completeness approach', 'completeness score',
             'completeness software', 'conductivity', 'contamination score', 'contamination screening input',
             'contamination screening parameters', 'culture rooting medium', 'current land use', 'current vegetation',
             'current vegetation method', 'decontamination software', 'density', 'depth', 'dermatology disorder',
             'detection type', 'dew point', 'diether lipids', 'dissolved carbon dioxide', 'dissolved hydrogen',
             'dissolved inorganic carbon', 'dissolved inorganic nitrogen', 'dissolved inorganic phosphorus',
             'dissolved organic carbon', 'dissolved organic nitrogen', 'dissolved oxygen', 'dominant hand', 'douche',
             'downward PAR', 'drainage classification', 'drug usage', 'efficiency percent', 'elevation', 'emulsions',
             'encoded traits', 'environmental medium', 'estimated size', 'ethnicity', 'experimental factor',
             'extrachromosomal elements', 'extreme_unusual_properties/Al saturation',
             'extreme_unusual_properties/Al saturation method', 'extreme_unusual_properties/heavy metals',
             'extreme_unusual_properties/heavy metals method', 'feature prediction', 'fertilizer regimen',
             'filter type', 'fluorescence', 'fungicide regimen', 'gaseous environment', 'gaseous substances',
             'gastrointestinal tract disorder', 'genetic modification', 'geographic location (latitude and longitude)',
             'glucosidase activity', 'gravidity', 'gravity', 'growth facility', 'growth habit',
             'growth hormone regimen', 'gynecological disorder', 'heating and cooling system type', 'herbicide regimen',
             'history/agrochemical additions', 'history/crop rotation', 'history/extreme events', 'history/fire',
             'history/flooding', 'history/previous land use', 'history/previous land use method', 'history/tillage',
             'host HIV status', 'host age', 'host blood pressure diastolic', 'host blood pressure systolic',
             'host body habitat', 'host body product', 'host body site', 'host body temperature',
             'host body-mass index', 'host color', 'host common name', 'host diet', 'host disease status',
             'host dry mass', 'host genotype', 'host growth conditions', 'host height', 'host last meal', 'host length',
             'host life stage', 'host occupation', 'host phenotype', 'host prediction approach',
             'host prediction estimated accuracy', 'host pulse', 'host scientific name', 'host sex', 'host shape',
             'host subject id', 'host subspecific genetic lineage', 'host substrate', 'host taxid', 'host total mass',
             'host wet mass', 'humidity', 'humidity regimen', 'hysterectomy', 'indoor space', 'indoor surface',
             'industrial effluent percent', 'inorganic particles', 'isolation and growth condition',
             'known pathogenicity', 'library reads sequenced', 'library screening strategy', 'library size',
             'library vector', 'light intensity', 'light regimen', 'light type', 'link to classification information',
             'link to climate information', 'links to additional analysis', 'liver disorder',
             'local environmental context', 'lung/pulmonary disorder', 'magnesium',
             'major diet change in last six months', 'mean friction velocity', 'mean peak friction velocity',
             'mechanical damage', 'medical history performed', 'menarche', 'menopause', 'methane', 'microbial biomass',
             'microbial biomass method', 'mineral nutrient regimen', 'multiplex identifiers', 'n-alkanes',
             'negative control type', 'nitrate', 'nitrite', 'nitrogen', 'non-mineral nutrient regimen',
             'nucleic acid amplification', 'nucleic acid extraction', 'number of replicons',
             'number of standard tRNAs extracted', 'observed biotic relationship', 'occupancy at sampling',
             'occupant density at sampling', 'organic carbon', 'organic matter', 'organic nitrogen',
             'organic particles', 'organism count', 'oxygen', 'oxygenation status of sample', 'pH', 'pH method',
             'pH regimen', 'particulate organic carbon', 'particulate organic nitrogen', 'pcr conditions',
             'pcr primers', 'perturbation', 'pesticide regimen', 'petroleum hydrocarbon', 'phaeopigments', 'phosphate',
             'phospholipid fatty acid', 'photon flux', 'plant growth medium', 'plant product', 'plant sex',
             'plant structure', 'ploidy', 'pollutants', 'pooling of DNA extracts (if done)', 'positive control type',
             'potassium', 'pre-treatment', 'predicted genome structure', 'predicted genome type', 'pregnancy',
             'presence of pets or farm animals', 'pressure', 'primary production', 'primary treatment',
             'profile position', 'project name', 'propagation', 'radiation regimen', 'rainfall regimen', 'reactor type',
             'reassembly post binning', 'redox potential', 'reference database(s)', 'reference for biomaterial',
             'relationship to oxygen', 'relative air humidity', 'relevant electronic resources',
             'relevant standard operating procedures', 'rooting conditions', 'rooting medium carbon',
             'rooting medium macronutrients', 'rooting medium micronutrients', 'rooting medium organic supplements',
             'rooting medium pH', 'rooting medium regulators', 'rooting medium solidifier', 'salinity', 'salt regimen',
             'sample capture status', 'sample collection device', 'sample collection method', 'sample disease stage',
             'sample material processing', 'sample size sorting method', 'sample storage duration',
             'sample storage location', 'sample storage temperature', 'sample volume or weight for DNA extraction',
             'seasonal environment', 'secondary treatment', 'sequence quality check', 'sequencing method',
             'sewage type', 'sexual activity', 'silicate', 'similarity search method', 'size fraction selected',
             'slope aspect', 'slope gradient', 'sludge retention time', 'smoker', 'sodium', 'soil horizon', 'soil pH',
             'soil texture method', 'soil type', 'soil type method', 'soil_taxonomic/FAO classification',
             'soil_taxonomic/local classification', 'soil_taxonomic/local classification method', 'solar irradiance',
             'soluble inorganic material', 'soluble organic material', 'soluble reactive phosphorus',
             'sorting technology', 'source material identifiers', 'source of UViGs', 'space typical state',
             'special diet', 'standing water regimen', 'study completion status', 'subspecific genetic lineage',
             'substructure type', 'sulfate', 'sulfide', 'surface humidity', 'surface material', 'surface moisture',
             'surface moisture pH', 'surface temperature', 'suspended particulate matter', 'suspended solids',
             'tRNA extraction software', 'target gene', 'target subfragment', 'taxonomic classification',
             'taxonomic identity marker', 'temperature', 'tertiary treatment', 'tidal stage',
             'time since last toothbrushing', 'time since last wash', 'tissue culture growth media', 'total carbon',
             'total depth of water column', 'total dissolved nitrogen', 'total inorganic nitrogen',
             'total organic carbon', 'total particulate carbon', 'total phosphate', 'total phosphorus',
             'travel outside the country in last six months', 'trophic level', 'turbidity', 'twin sibling presence',
             'typical occupant density', 'urine/collection method', 'urine/kidney disorder',
             'urine/urogenital tract disorder', 'urogenital disorder', 'ventilation rate', 'ventilation type',
             'viral identification software', 'virus enrichment approach', 'volatile organic compounds',
             'wastewater type', 'water content', 'water content method', 'water current', 'water temperature regimen',
             'watering regimen', 'weight loss in last three months', 'wind direction', 'wind speed'])
        self.assertListEqual(self.pairwise_obj.get_left_exact_matched_list(), test_out)


    def test_get_left_harmonised_matched_list(self):
        test_out = sorted(['Depth', 'Salinity', 'Sample Collection Device', 'Size Fraction Lower Threshold',
         'Size Fraction Upper Threshold', 'Temperature', 'host family relationship', 'surface air contaminant'])
        self.assertListEqual(self.pairwise_obj.get_left_harmonised_matched_list(), test_out)

    def test_get_left_fuzzy_matched_list(self):
        test_out = sorted(['16S recovered', '16S recovery software', 'Chlorophyll Sensor', 'DNA concentration', 'Event Date/Time End', 'Event Date/Time Start', 'Event Label', 'GAL_sample_id', 'Last Update Date', 'Latitude End', 'Latitude Start', 'Longitude End', 'Longitude Start', 'Marine Region', 'Nitrate Sensor', 'Oxygen Sensor', 'Salinity Sensor', 'Sample Status', 'Sampling Campaign', 'Sampling Platform', 'Sampling Site', 'Sampling Station', 'UViG assembly quality', 'WHO/OIE/FAO clade (required for HPAI H5N1 viruses)', 'adductor weight', 'age', 'air temperature', 'annotation source', 'antiviral treatment dosage', 'antiviral treatment duration', 'antiviral treatment initiation', 'aquaculture origin', 'area of sampling site', 'bio_material', 'biotic relationship', 'cell_line', 'cell_type', 'chemical compound', 'collected_by', 'collector name', 'composite design/sieving (if any)', 'country of travel', 'culture_collection', 'date of birth', 'date of death', 'definition for seropositive sample', 'dev_stage', 'diagnostic method', 'disease staging', 'engrafted tumor collection site', 'engrafted tumor sample passage', 'engraftment host strain name', 'environmental history', 'environmental package', 'environmental stress', 'environmental_sample', 'experimental factor 1', 'experimental factor 2', 'experimental factor 3', 'experimental factor 4', 'experimental factor 5', 'genotype', 'geographic location (country and/or sea)', 'geographic location (latitude)', 'geographic location (longitude)', 'geographic location (region and locality)', 'gonad weight', 'growth condition', 'growth media', 'habitat', 'health or disease status of specific host', 'host behaviour', 'host breed', 'host description', 'host diet treatment', 'host diet treatment concentration', 'host disease outcome', 'host disease stage', 'host gutted mass', 'host habitat', 'host health state', 'host storage container', 'host storage container pH', 'host storage container temperature', 'identified_by', 'illness duration', 'illness onset date', 'individual', 'infect', 'influenza strain unique number', 'influenza test method', 'influenza test result', 'influenza vaccination date', 'influenza vaccination type', 'influenza virus type', 'influenza-like illness at the time of sample collection', 'initial time point', 'inoculation dose', 'inoculation route', 'instrument for DNA concentration measurement', 'investigation type', 'isolation source host-associated', 'isolation_source', 'lab_host', 'library construction method', 'lineage:swl (required for H1N1 viruses)', 'lung/nose-throat disorder', 'mating_type', 'mean annual and seasonal precipitation', 'mean annual and seasonal temperature', 'meaning of cut off value', 'metagenomic source', 'nose/mouth/teeth/throat disorder', 'number of inoculated individuals', 'organism common name', 'organism part', 'organism phenotype', 'original collection date', 'original geographic location', 'original geographic location (latitude)', 'original geographic location (longitude)', 'other pathogens test result', 'other pathogens tested', 'passage_history', 'patient age at collection of tumor', 'patient sex', 'patient tumor diagnosis at time of collection', 'patient tumor primary site', 'patient tumor site of collection', 'patient tumor type', 'personal protective equipment', 'phenotype', 'plant body site', 'plant developmental stage', 'plant treatment', 'population size of the catchment area', 'protocol', 'read quality filter', 'receipt date', 'reference host genome for decontamination', 'relationship', 'replicate', 'salinity method', 'sample collection device or method', 'sample coordinator', 'sample coordinator affiliation', 'sample derived from', 'sample disease status', 'sample dry mass', 'sample health state', 'sample height', 'sample length', 'sample material', 'sample origin', 'sample phenotype', 'sample same as', 'sample storage buffer', 'sample storage conditions', 'sample storage container', 'sample symbiont of', 'sample taxon name', 'sample transportation date', 'sample transportation temperature', 'sample transportation time', 'sample unique ID', 'sample weight for DNA extraction', 'sample wet mass', 'sampled age', 'sampling time point', 'serotype', 'serotype (required for a seropositive sample)', 'serovar', 'serovar_in-silico', 'sex', 'shellfish soft tissue weight', 'shellfish total weight', 'single cell or viral particle lysis approach', 'single cell or viral particle lysis kit protocol', 'size of the catchment area', 'soil horizon method', 'soil texture measurement', 'soil water content', 'source material description', 'source of vaccination information', 'specific host', 'specimen_id', 'storage conditions (fresh/frozen/other)', 'strain', 'sub_group', 'sub_strain', 'sub_type', 'subject exposure', 'subject exposure duration', 'subspecific genetic lineage name', 'subspecific genetic lineage rank', 'surveillance target', 'symbiont', 'time', 'tissue_lib', 'tissue_type', 'total nitrogen', 'total nitrogen method', 'total organic C method', 'travel-relation', 'treatment agent', 'treatment date', 'treatment dose', 'trial timepoint', 'type exposure', 'vaccine lot number', 'virus identifier', 'was the PDX model humanised?'])
        self.assertListEqual(self.pairwise_obj.get_left_fuzzy_matched_list(), test_out)

    def test_get_left_confident_matched_list(self):
        self.assertEqual(len(self.pairwise_obj.get_left_confident_matched_list()), 367)

    def test_get_left_not_matched_list(self):

        test_out = sorted(['Citation', 'Further Details', 'GAL', 'Protocol Label', 'antiviral treatment', 'barcoding center', 'block', 'cellular component', 'clinical setting', 'collecting institution', 'cultivar', 'diagnosis', 'dose', 'ecotype', 'finishing strategy', 'germline', 'hospitalisation', 'identifier_affiliation', 'illness symptoms', 'immunoprecipitate', 'inoculation stock availability', 'isolate', 'lifestage', 'pathotype', 'proxy biomaterial', 'proxy voucher', 'seabed habitat', 'shell length', 'shell markings', 'shell width', 'specimen_voucher', 'sub_species', 'tolid', 'toxin burden', 'trial length', 'vaccine dosage', 'vaccine manufacturer', 'variety'])
        self.assertListEqual(self.pairwise_obj.get_left_not_matched_list(), test_out)

    def test_get_right_exact_matched_list(self):
        self.assertListEqual(sorted(self.pairwise_obj.get_right_exact_matched_list()), sorted(self.pairwise_obj.get_left_exact_matched_list()))

    def test_get_right_harmonised_matched_list(self):
         self.assertEqual(len(self.pairwise_obj.get_right_harmonised_matched_list()), len(self.pairwise_obj.get_left_harmonised_matched_list()))

    def test_get_right_fuzzy_matched_list(self):
        self.assertEqual(len(self.pairwise_obj.get_right_fuzzy_matched_list()), 109)


    def test_get_right_confident_matched_list(self):
        self.assertEqual(len(self.pairwise_obj.get_right_confident_matched_list()), 367)


    def test_get_right_not_matched_list(self):
        #print(f"right_not_matched_list() len={len(self.pairwise_obj.get_right_not_matched_list())}")
        # print(self.pairwise_obj.get_right_not_matched_list())
        self.assertEqual(len(self.pairwise_obj.get_right_fuzzy_matched_list()), 109)

    # def test_get_any_left_match_list(self):
    #     self.fail()

if __name__ == '__main__':
    unittest.main()