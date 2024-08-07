export interface Adventure {
    name: string
    tier: number
    dms: string[]
    players: string[]
}

export interface Character {
    name: string
    race: CategoryClass
    subrace: CategoryClass
    classes: PlayerClass[]
    level?: number
}

export interface Races {
    id: number
    value: string
    subraces: CategoryClass[]
}

export interface PlayerClass {
    id: number
    value: string
    subclasses: CategoryClass[]
}

export interface CategoryClass {
    id: number
    value: string
}

export interface Counts {
    [key: string]: number
}

export interface Item {
    id: number
    name: string
    table: string
    type: CategoryClass
    cost: number
    rarity: CategoryClass
    attunement: boolean
    item_modifier: boolean
    seeking_only: boolean
    school: CategoryClass
    source: string
    level: number
    classes: CategoryClass[]
    notes: string
}