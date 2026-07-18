from ecs.components.job import Job
from ecs.components.hunger import Hunger
from ecs.systems.hunger_rules import hunger_rules
from ecs.systems.work_rules import work_rules
from logger_config import get_logger

logger = get_logger(__name__)

class AISystem:
    def __init__(self, world, map_data, spawner):
        self.world = world
        self.map = map_data
        self.spawner = spawner

        # Order matters. Survival dictates behavior before productivity.
        self.priority_rule_sets = [
            ("Survival", hunger_rules),
            ("Productivity", work_rules),
        ]

    def update(self):
        # Fetch entities. If this returns empty, the loop never runs.
        entities_with_hunger = self.world.get_entity_with(Hunger)
        logger.info(f"Entities with Hunger: {entities_with_hunger}")

        for entity in entities_with_hunger:
            # Skip decision making if they are already working on a valid job
            logger.debug(f"Evaluating entity {entity}...")
            if self.world.has_component(entity, Job):
                logger.info(f"Entity {entity} already has an active Job {self.world.get_component(entity,Job).job}. Skipping.")
                continue

            logger.info(f"Entity {entity} is idle. Evaluating new jobs...")
            self.assign_optimal_job(entity)

    def assign_optimal_job(self, entity):
        hunger_comp = self.world.get_component(entity, Hunger)

        if not hunger_comp:
            logger.info(f"Entity {entity} has no Hunger component despite being queried for it.")
            return

        is_starving = hunger_comp.hunger < 10
        logger.info(f"Entity {entity} hunger level: {hunger_comp.hunger}. Starving status: {is_starving}")

        for category, rules in self.priority_rule_sets:
            # Prevent entities from working if they are starving
            if category == "Productivity" and is_starving:
                logger.warning(f"Entity {entity} is starving. Skipping Productivity rules.")
                continue 

            for rule in rules:
                logger.info(f"Entity {entity} evaluating rule: {rule.__name__}")
                jobs = rule(entity, self.world,self.spawner)

                if jobs:
                    logger.info(f"Entity {entity} selected jobs from {rule.__name__}: {jobs}")
                    self.apply_job_stack(entity, jobs)
                    return # Exit out completely once a job path is locked in

        logger.debug(f"Entity {entity} found no valid jobs to execute. Remaining idle.")

    def apply_job_stack(self, entity, jobs):
        # Applies jobs sequentially. 
        # The final overwrite ensures the most immediate prerequisite is processed first.
        for job_data in jobs:
            new_job = Job(job_data)
            if self.world.has_component(entity, Job):
                logger.info(f"Entity {entity} updating Job to prerequisite: {job_data.get('type')}")
                self.world.update_component(entity, new_job)
            else:
                logger.info(f"Entity {entity} assigning base Job: {job_data.get('type')}")
                self.world.add_component(entity, new_job)


    def pseudo_update(self):
        self.world.add_component(52,Job({"type":"Gather","target":2,"priority":90}))
        self.world.update_component(52,Job({"type":"Gather","target":63,"priority":30}))