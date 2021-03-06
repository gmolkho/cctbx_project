from __future__ import print_function, division
from xfel.merging.application.worker import worker

class reflection_table_editor(worker):
  """
  Add and/or remove columns in the reflection table
  """

  def add_asu_miller_indices_column(self, experiments, reflections):
    '''Add a "symmetry-reduced hkl" column to the reflection table'''
    if reflections.size() == 0:
      return

    from cctbx import miller
    from cctbx.crystal import symmetry
    import copy

    # assert that the space group used to integrate the data is consistent with the input space group for merging

    #target_patterson_group_info = target_space_group.build_derived_patterson_group().info().symbol_and_number()

    # build target space group and target patterson group info
    target_unit_cell = self.params.scaling.unit_cell
    target_space_group_info = self.params.scaling.space_group
    target_symmetry = symmetry(unit_cell=target_unit_cell, space_group_info=target_space_group_info)
    target_space_group = target_symmetry.space_group()
    target_patterson_group_info = target_space_group.build_derived_patterson_group().info().symbol_and_number()

    for experiment in experiments:
      experiment_patterson_group_info = experiment.crystal.get_space_group().build_derived_patterson_group().info().symbol_and_number()
      if target_patterson_group_info != experiment_patterson_group_info:
        assert False, "Target patterson group %s is different from an experiment patterson group %s"%(target_patterson_group_info, experiment_patterson_group_info)

    # add a new hkl column
    reflections['miller_index_asymmetric'] = copy.deepcopy(reflections['miller_index'])
    miller.map_to_asu(target_space_group.type(),
                      not self.params.merging.merge_anomalous,
                      reflections['miller_index_asymmetric'])

  def prune_reflection_columns(self, reflections):
    '''Remove reflection table columns which are not relevant to merging'''
    if reflections.size() == 0:
      return

    all_keys = list()
    for key in reflections[0]:
      all_keys.append(key)

    for key in all_keys:
      if key != 'intensity.sum.value' and key != 'intensity.sum.variance' and key != 'miller_index_asymmetric' and key != 'id':
        del reflections[key]

  def run(self, experiments, reflections):

    self.logger.log_step_time("ADD_ASU_HKL_COLUMN")
    self.add_asu_miller_indices_column(experiments, reflections)
    self.logger.log_step_time("ADD_ASU_HKL_COLUMN", True)

    self.logger.log_step_time("PRUNE_COLUMNS")
    self.prune_reflection_columns(reflections)
    self.logger.log_step_time("PRUNE_COLUMNS", True)

    return experiments, reflections
